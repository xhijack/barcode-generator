import hashlib
from io import BytesIO
import frappe
import qrcode


@frappe.whitelist(allow_guest=True)
def generate_barcode(item_code, barcode_type="Code128", width=0.4, height=None, scale=None):
    # Write to a file-like object:
    # Or to an actual file:
    from barcode import Code128
    from barcode.writer import SVGWriter
    filename = hashlib.md5(item_code.encode()).hexdigest()
    if barcode_type == "Code128":
        options = {
            'module_width': width,  # Lebar setiap modul (garis)
            'quiet_zone': 10       # Jarak kosong di sekitar barcode
        }
        with open("{}/public/files/barcode/{}.svg".format(frappe.local.site,filename), "wb") as f:
            Code128(str(item_code), writer=SVGWriter()).write(f, options)
            # return """<img src="http://localhost:8006/files/barcode/{}.svg" alt="barcode" style="width:100%;height:100%;">""".format(filename)
            return "/files/barcode/{}.svg".format(filename)
    else:
        raise Exception("Barcode type not supported")

def generate_qr_code(item_code):
    qr = qrcode.QRCode(
        version=1,  # Versi QR Code (1-40), semakin besar semakin besar ukuran QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Tingkat koreksi kesalahan
        box_size=10,  # Ukuran setiap "box" (piksel) dalam QR Code
        border=1,  # Ukuran margin (border) dalam "box" (piksel)
    )

    qr.add_data(item_code)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    filename = hashlib.md5(item_code.encode()).hexdigest()
    img.save("{}/public/files/barcode/{}.png".format(frappe.local.site,filename))
    return "/files/barcode/{}.png".format(filename)
    # return """<img src="/files/barcode/{}.png" alt="barcode" style="width:100%;height:100%;">""".format(filename)
