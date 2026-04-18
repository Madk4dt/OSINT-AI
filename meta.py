# meta.py
from utils import t
from config import SOURCES_DB

def meta_file(filepath):
    lines = [t("meta_title", filepath), ""]
    try:
        import exifread
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f)
            if tags:
                lines.append(t("meta_exif"))
                for tag in list(tags.keys())[:10]:
                    lines.append(f"  {tag}: {tags[tag]}")
    except ImportError:
        lines.append("exifread not installed. pip install exifread")
    except Exception as e:
        lines.append(t("meta_error", str(e)))
    try:
        import PyPDF2
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            info = reader.metadata
            if info:
                lines.append(t("meta_pdf"))
                for k,v in info.items():
                    lines.append(f"  {k}: {v}")
    except ImportError:
        pass
    except:
        pass
    return "\n".join(lines), SOURCES_DB.get("meta", [])