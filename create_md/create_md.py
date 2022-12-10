class CreateMdFile():
    def __init__(self, client_name):
        self.path = "/output/text.md"
        self.client_name = client_name


    def create_mdfile_head(self):
        with open(self.path, mode = 'w') as f:
            f.write("---\n"
                    "marp: true\n"
                    "theme: gaia\n"
                    f'header: "{self.client_name}様宛"\n'
                    'footer: "by terasawa_yasuto"\n'
                    "---\n"
                    "# 老後の人生設計プラン\n"
                    "---\n")

    def create_page(self, image_path):
        with open(self.path, mode = "a") as f:
            for k, i in kwargs.items:
                f.write(f"- {k} : {i}\n")
            
            f.write("![bg left:40%](output/{image_path}.jpeg)\n"
                    "---\n")