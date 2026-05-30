from app.renderer.html_renderer import render_all_pages


def test_render_all_pages_minimal():
    proposal = {
        "proposalMeta": {"clientCompanyName": "Test"},
        "services": [],
        "combinedPricing": {"includedServices": []},
    }
    files = render_all_pages(proposal, "TEST-ID")
    assert len(files) == 2
