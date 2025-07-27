# 🏆 Automated Certificate Generator

**Bulk-generate professional, high-resolution (2000x1414 pixels) course completion certificates — effortlessly and automatically!**

## 🚀 Features

- **Bulk Certificate Generation**: Create hundreds/thousands of certificates from a CSV.
- **Template Flexibility**: Use your own custom PNG template, sized for print (2000x1414 px).
- **PDF & PNG Output**: Save certificates as high-quality PDFs, PNGs, or both.
- **Automatic Data Insertion**: Fill in names, courses, and dates automatically.
- **Custom Fonts**: Use beautiful fonts like _Great Vibes_ or supply your own.
- **Easy Configuration**: All settings in a single YAML file—adjust size, font, placement, paths, output.
- **Extensible**: Ready to adapt for more data, API, or database use.

## 📦 Project Structure
certificate_generator/ \
├── src/ # Core logic (certificate generation, data handler, etc.) \
│ ├── certificate_generator.py\
│ └── data_handler.py\
├── config/\
│ └── config.yaml # All your settings\
├── data/\
│ └── participants.csv # Your recipient list\
├── templates/\
│ └── template.png # Your certificate design (2000x1414px)\
├── fonts/\
│ └── GreatVibes-Regular.ttf\
├── output/certificates/ # Where your results go\
├── main.py\
├── font_downloader.py\
├── requirements.txt\
└── README.md

## 🛠️ Installation

1. **Clone or download this repo**
2. **Install dependencies**

```bash
 pip install -r requirements
```

3. **Download the font**
```bash
 python font_downloader.py
```
4. **Place your template**
- Use a 2000x1414 px PNG in `templates/template.png`
5. **Edit your participant list**
- Open `data/participants.csv`, or a sample will be generated automatically
6. **Check `config/config.yaml`**
- Set `width: 2000` and `height: 1414` under `certificate:`
- Make further adjustments as needed

## ⚙️ Configuration

All settings are in `config/config.yaml`. Example settings for your high-res template:

```bash
certificate:
template_path: "./templates/template.png"
output_path: "./output/certificates/"
width: 2000
height: 1414
background_color: "#FFFFFF"

fonts:
default_font: "./fonts/GreatVibes-Regular.ttf"
title_font_size: 130
name_font_size: 180
details_font_size: 60
font_color: "#1A1A1A"

data:
csv_path: "./data/participants.csv"
required_columns: ["name", "course", "completion_date"]

positioning:
title_y: 350
name_y: 600
course_y: 900
date_y: 1150

output:
format: "both" # "pdf", "png", or "both"
quality: 95
dpi: 300
```


⚠️ **Tip:** Adjust the numeric "positioning" values to match where things fit on your template!

## 📑 Usage
```bash
python main.py
```

- Loads your CSV data
- Inserts dynamic content onto your template
- Saves each certificate to `output/certificates/` as PDF and/or PNG

## 👤 Data Format

`data/participants.csv` (headers should be: `name,course,completion_date`):

```bash
name,course,completion_date
Name Example,Python Basics,July 25 2025
```

## 🎨 Customization

- **Design:** Use design software (Canva, Figma, Photoshop, etc) to make a PNG (2000x1414 px) template
- **Font:** Replace the font in the `fonts/` folder and point to your `.ttf` in `config.yaml`
- **Field Positioning:** Adjust y-coordinates for each field in the config until happy

## 🩹 Troubleshooting

| Problem                | Tip                                              |
|------------------------|--------------------------------------------------|
| Config file not found  | Make sure `config/config.yaml` exists            |
| Font not found         | Run `python font_downloader.py`                  |
| Wrong output paths     | Check your `output_path` in config.yaml          |
| Text not aligned       | Tweak "positioning" coordinates                  |
| CSV issues             | Make sure your CSV has header: name,course,date  |


## 🧑‍💻 Contributing

Pull requests and issues welcome! Ideas for features, bug fixes, and template contributions are appreciated.

## 📜 License

MIT License — Free for all personal and commercial use.

