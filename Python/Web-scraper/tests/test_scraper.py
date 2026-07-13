from infrastructure.scraper import BeautifulSoupQuoteScraper

SAMPLE_HTML = """
<div class="quote">
    <span class="text">"La vida es lo que pasa mientras estás ocupado haciendo otros planes."</span>
    <small class="author">John Lennon</small>
    <div class="tags">
        <a class="tag">vida</a>
        <a class="tag">planes</a>
    </div>
</div>
"""


def test_parse_quote_extracts_text_author_and_tags():
    quotes = BeautifulSoupQuoteScraper._parse_quotes(SAMPLE_HTML)

    assert len(quotes) == 1
    quote = quotes[0]
    assert "vida" in quote.text.lower()
    assert quote.author == "John Lennon"
    assert quote.tags == ["vida", "planes"]


def test_parse_quote_returns_empty_list_when_no_quotes():
    quotes = BeautifulSoupQuoteScraper._parse_quotes("<html><body></body></html>")
    assert quotes == []