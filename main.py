from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from color_handler import PaletteGenerator
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/images"

app = Flask(__name__)
app.config["SECRET_KEY"] = "happy-me"
Bootstrap(app)


def remove_files(directory):
    files = os.listdir(directory)
    for f in files:
        os.remove(f"{directory}/{f}")
    return files


class PhotoForm(FlaskForm):
    style = {'class': 'ourClasses btn btn-dark', 'style': 'margin: 1%;'}
    photo = FileField(validators=[FileRequired(), FileAllowed(["jpg", "png", "jpeg"], "Images only!")], render_kw=style)
    submit = SubmitField("submit", render_kw=style)


@app.route("/", methods=["GET", "POST"])
def home():
    form = PhotoForm()
    color_palette = []
    all_files = None
    if form.validate_on_submit():
        form = PhotoForm()
        # deleting previously loaded images
        remove_files("static/images")
        # getting and securing the image.
        f = request.files["photo"]
        filename = secure_filename(f.filename)
        print(filename)
        # adding the new image to directory
        f.save(os.path.join("static/images", filename))
        # generating the palette
        plt_gnr = PaletteGenerator(f)
        plt_gnr.get_pixels()
        color_palette = plt_gnr.top_colors
        # getting the only image in te directory. There is only one img cuz we deleted the rest first.
        all_files = os.listdir("static/images")

    return render_template("index.html", form=form, color_palette=color_palette, all_files=all_files)


@app.route("/upload/<filename>")
def get_file(filename):
    print(f"get file method: {send_from_directory('static/images', filename)}")
    return send_from_directory("static/images", filename)


if __name__ == "__main__":
    app.run(debug=True)
