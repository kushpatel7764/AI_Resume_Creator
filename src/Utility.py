import subprocess


def string_to_array(string):
    stripped_string = string.strip()
    array = []
    for item in stripped_string.split(','):
        # Remove white space the append to array
        array.append(item.strip())
    return array


def array_to_string(array):
    # array is an array of tuples
    string = ''
    for i, item in enumerate(array):
        if len(array) == i + 1:
            string += str(item[0])
        else:
            string += str(item[0]) + ", "
    return string


def user_profile_to_paragraph(profile, projects, classes):
    return_str = f"""My name is {profile.name}. Some important courses I have completed at BSU are {classes}. Additionally'
                , along with my courses, I have also  done projects such as {projects}. Some ways to contact me are
                through my email: {profile.email}, phone: {profile.phone}, github: {profile.github}, linkedin:
                 {profile.linkedin}. Some other important information about me is {profile.other}"""
    return return_str


def user_profile_to_keywords(profile, projects, classes):
    return_str = ""
    # AI does not need the profile id
    if "id" in profile:
        profile.pop("id")

    for key, value in profile.items():
        return_str += key + ": " + str(value) + "\n"
    return_str += "Projects: " + projects + "\n"
    return_str += "Classes: " + classes
    return return_str


def convert_markdown_to_pdf(markdown_file, output_pdf):
    try:
        subprocess.run(["markdown-pdf", markdown_file, "-o", output_pdf], check=True)
        print(f"PDF saved successfully as: {output_pdf}")
    except Exception as e:
        print(f"Error converting Markdown to PDF: {e}")
