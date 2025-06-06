from flask import Flask, render_template, request
from search_engine import IRSystem  # Make sure your IR system class is correctly implemented

app = Flask(__name__)
search_engine = IRSystem("documents")  # Path to XML or other files

# Recursively convert defaultdict to regular dicts for Jinja compatibility
def convert_defaultdict_to_dict(obj):
    if isinstance(obj, dict):
        return {k: convert_defaultdict_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_defaultdict_to_dict(i) for i in obj]
    return obj

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    paginated_results = []
    snippets = {}
    stats = {"query_terms": [], "TF": {}, "IDF": {}, "TFIDF": {}}
    headers = search_engine.get_headers()
    documents = search_engine.get_documents()

    # Handle pagination parameters
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    per_page = 30

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            ranked, snippets, scores, raw_stats = search_engine.search(query)
            stats = convert_defaultdict_to_dict(raw_stats)
            results = list(ranked.items())

            # Pagination logic
            total_pages = (len(results) + per_page - 1) // per_page
            page = min(page, total_pages) if total_pages > 0 else 1
            start = (page - 1) * per_page
            end = start + per_page
            paginated_results = results[start:end]

            # Smart pagination range (e.g., max 5 pages shown)
            start_page = max(1, page - 2)
            end_page = min(total_pages, page + 2)
        else:
            total_pages = 0
            start_page = 1
            end_page = 1
    else:
        total_pages = 0
        start_page = 1
        end_page = 1

    return render_template("index.html",
                           query=query,
                           results=paginated_results,
                           snippets=snippets,
                           stats=stats,
                           documents=documents,
                           headers=headers,
                           current_page=page,
                           total_pages=total_pages,
                           start_page=start_page,
                           end_page=end_page)

if __name__ == "__main__":
    app.run(debug=True)
