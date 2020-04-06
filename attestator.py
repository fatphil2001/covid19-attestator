#!/usr/bin/env python3
# -*- coding:utf-8 -*
#
# Skia < skia AT libskia DOT so >
#
# Beerware licensed software - 2020
#

from pprint import pprint
from datetime import datetime, timedelta

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

user_data = {
    "first_name": "Jean",
    "last_name": "Dupont",
    "birth_year": 1970,
    "birth_month": 1,
    "birth_day": 1,
    "birth_place": "Lyon",
    "address": "999 avenue de france",
    "zip_code": "71000",
    "city": "Paris",
    "reasons": [],
    "trip_datetime": datetime.now() + timedelta(minutes=10),
}

reasons = {
    "travail": 18.6,
    "courses": 16.85,
    "sante": 15.4,
    "famille": 14.1,
    "sport": 12.15,
    "judiciaire": 10.5,
    "missions": 9.2,
}

now = datetime.now()


def generate_pdf(user_data):
    c = canvas.Canvas("attestation.pdf")

    im = ImageReader("bg.png")
    width, height = im.getSize()
    size = max(width, height)
    width = 8 * cm * width / size
    height = 8 * cm * height / size
    c.drawImage(im, 0, 0, 21 * cm, 29.7 * cm)

    c.drawString(  # "Je soussigné"
        4.4 * cm, 24.2 * cm, user_data["first_name"] + " " + user_data["last_name"]
    )
    c.drawString(  # "Né le"
        4.4 * cm,
        23.33 * cm,
        "%02d/%02d/%d"
        % (user_data["birth_day"], user_data["birth_month"], user_data["birth_year"]),
    )
    c.drawString(3.3 * cm, 22.52 * cm, user_data["birth_place"])  # "à"
    c.drawString(  # "Demeurant"
        4.72 * cm,
        21.62 * cm,
        user_data["address"] + " " + user_data["zip_code"] + " " + user_data["city"],
    )

    c.drawString(3.9 * cm, 7.97 * cm, user_data["city"])  # "Fait à"

    c.drawString(  # "Le"
        3.3 * cm,
        7.08 * cm,
        "%02d/%02d/%d"
        % (
            user_data["trip_datetime"].day,
            user_data["trip_datetime"].month,
            user_data["trip_datetime"].year,
        ),
    )
    c.drawString(  # "à"
        7.00 * cm,
        7.08 * cm,
        "%02d   %02d"
        % (user_data["trip_datetime"].hour, user_data["trip_datetime"].minute),
    )

    c.setFont("Helvetica", 7)
    c.drawRightString(18.20 * cm, 5.3 * cm, "Date de création:")  # "Date de création"
    c.drawRightString(  # "XX/XX/XXXX à XXhXX"
        18.20 * cm,
        5.04 * cm,
        "%02d/%02d/%d à %02dh%02d"
        % (now.day, now.month, now.year, now.hour, now.minute),
    )

    c.setFont("Helvetica", 14)
    for reason in user_data["reasons"]:
        c.drawString(2.7 * cm, reasons[reason] * cm, "X")

    qrcode = generate_qrcode(user_data)

    bounds = qrcode.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    small_qr = Drawing(transform=[3.9 * cm / width, 0, 0, 3.9 * cm / height, 0, 0])
    small_qr.add(qrcode)

    renderPDF.draw(small_qr, c, 14.9 * cm, 5.26 * cm)

    c.showPage()

    big_qr = Drawing(transform=[11.7 * cm / width, 0, 0, 11.7 * cm / height, 0, 0])
    big_qr.add(qrcode)
    renderPDF.draw(big_qr, c, 1.3 * cm, 16.8 * cm)

    c.save()


def generate_qrcode(user_data):
    code = "; ".join(
        [
            "Cree le: %02d/%02d/%d a %02dh%02d"
            % (now.day, now.month, now.year, now.hour, now.minute),
            "Nom: " + user_data["last_name"],
            "Prenom: " + user_data["first_name"],
            "Naissance: %02d/%02d/%d a %s"
            % (
                user_data["birth_day"],
                user_data["birth_month"],
                user_data["birth_year"],
                user_data["birth_place"],
            ),
            "Adresse: %s %s %s"
            % (user_data["address"], user_data["zip_code"], user_data["city"]),
            "Sortie: %02d/%02d/%d a %02dh%02d"
            % (
                user_data["trip_datetime"].day,
                user_data["trip_datetime"].month,
                user_data["trip_datetime"].year,
                user_data["trip_datetime"].hour,
                user_data["trip_datetime"].minute,
            ),
            "Motifs: %s" % "-".join(user_data["reasons"]),
        ]
    )
    return QrCodeWidget(code)


def get_reason():
    print("Raisons de la sortie:")
    for reason in reasons:
        answer = input("%s ? (o/N) " % reason)
        if answer and answer[0].lower() in ["o", "y"]:
            user_data["reasons"].append(reason)


def main():
    get_reason()
    generate_pdf(user_data)


if __name__ == "__main__":
    main()
