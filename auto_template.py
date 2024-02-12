import markdown
import re
import os
# import arxiv


def get_markdown_table():
    with open('README.md', 'r') as f:
        text = f.read()
        md_table = markdown.markdown(text).split('|---|---|---|---|---|---|')[-1]
    return md_table

def write_markdown_table(new_md_table):
    before_table=''
    with open('README.md', 'r') as f:
        text = f.read()
        before_table = markdown.markdown(text).split('|---|---|---|---|---|---|')[0]
    with open('README.md', 'w', encoding='utf-8') as md_file:
        content=before_table+'\n|---|---|---|---|---|---|\n'+new_md_table
        md_file.write(content)

def get_markdown_list(md_table):
    lines = [line.strip() for line in md_table.split('\n') if line.strip() and not line.startswith('|---')]
    extracted_data = []
    for row in lines:
        columns = row.split('|')[1:-1][1]
        columns=columns.replace('</strong>','').replace('<strong>','')
        extracted_data.append(columns)
    return extracted_data

def change_title(list_title):
    new_title=[]
    for title in list_title:
        title=re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", title).replace(' ','-')
        new_title.append(title)
    return new_title

def get_title_directory(dir):
    titles = []
    for filename in os.listdir(dir):
        if filename.endswith('.md'):
            titles.append(filename.split('.md')[0])
    return titles

def check_duplicate(list_title, new_title, exist_title):
    """
    Store original title and reformed title as dict to retrieve.
    """
    dict_title={}
    for idx in range(len(list_title)):
        if new_title[idx] in exist_title:
            continue
        dict_title[list_title[idx]]=new_title[idx]
    return dict_title

def create_markdown_template(dict_title):
    for key,val in dict_title.items():
        content=f"# [TLDR] {key} \n "
        with open(f"./TLDR/{val}.md", 'w', encoding='utf-8') as file:
            file.write(content)

def make_md_table(md_table):
    lines = [line.strip() for line in md_table.split('\n') if line.strip() and not line.startswith('|---')]
    new_lines=[]
    for row in lines:
        _,date,title,authors,pdf,tags,tldr,_ = row.split('|')
        title = title.replace("</strong>", "").replace("<strong>", "")
        # if pdf=="":
        #     pdf=get_arxiv_link(title)
        if tldr=="":
            tldr=get_tldr_link(title)
        title = f"** {title} **"
        date = date.replace("</strong>", " **").replace("<strong>", "** ")
        new_lines.append(f"|{date}|{title}|{authors}|{pdf}|{tags}|{tldr}|")
    return '\n'.join(new_lines)


def get_arxiv_link(title):
    client = arxiv.Client()
    search = arxiv.Search(
        query=f"ti:'{title}'",
        max_results=1,
    )
    result=next(client.results(search))
    if result:
        return result.replace('/abs/','/pdf/')
    return ''

def get_tldr_link(title):
    new_title=change_title([title])[0]
    return f"./TLDR/{new_title}.md"

if __name__=="__main__":
    # Get title list from README.md table
    md_table=get_markdown_table()
    list_title=get_markdown_list(md_table)
    new_title=change_title(list_title)

    # Get exist md list in dir TLDR and make new md files
    exist_title=get_title_directory('./TLDR')
    dict_title=check_duplicate(list_title, new_title, exist_title)
    create_markdown_template(dict_title)

    # Fill the vacant columns of table
    # new_md_table=make_md_table(md_table)
    # write_markdown_table(new_md_table)