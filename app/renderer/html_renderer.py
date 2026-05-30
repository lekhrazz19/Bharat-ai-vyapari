from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STYLE_DIR = BASE_DIR / "styles"
OUTPUT_DIR = Path("storage/html")

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
)


def _copy_css(folder: Path) -> None:
    target = folder / ".." / "styles"
    target.mkdir(parents=True, exist_ok=True)
    css_source = STYLE_DIR / "proposal.css"
    (target / "proposal.css").write_text(css_source.read_text(encoding="utf-8"), encoding="utf-8")


def render_template(template_name: str, data: dict, output_path: Path) -> str:
    template = env.get_template(template_name)
    html = template.render(**data)
    output_path.write_text(html, encoding="utf-8")
    return str(output_path)


def render_all_pages(proposal: dict, proposal_id: str) -> list[str]:
    folder = OUTPUT_DIR / proposal_id
    folder.mkdir(parents=True, exist_ok=True)
    _copy_css(folder)
    files = []

    files.append(render_template("cover.html", proposal, folder / "page-00-cover.html"))
    page_number = 1

    for service in proposal.get("services", []):
        data = {"proposalMeta": proposal.get("proposalMeta", {}), "service": service, "pageNumber": page_number}
        files.append(render_template("service_intro.html", data, folder / f"page-{page_number:02d}-intro.html"))
        page_number += 1

        data["pageNumber"] = page_number
        files.append(render_template("workflow.html", data, folder / f"page-{page_number:02d}-workflow.html"))
        page_number += 1

        data["pageNumber"] = page_number
        files.append(render_template("benefits_pas.html", data, folder / f"page-{page_number:02d}-benefits.html"))
        page_number += 1

    files.append(render_template(
        "combined_pricing.html",
        {
            "proposalMeta": proposal.get("proposalMeta", {}),
            "combinedPricing": proposal.get("combinedPricing", {}),
            "pageNumber": page_number,
        },
        folder / f"page-{page_number:02d}-pricing.html",
    ))
    return files
