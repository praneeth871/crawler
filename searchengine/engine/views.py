from django.http import HttpResponse
from django.template import Template, Context
import datetime
from django.template.loader import get_template
from pytz import timezone
import os
from operator import itemgetter


def index(request):
    return HttpResponse("Hello, world1. You're at the polls index.")


def current_time():
    return datetime.datetime.now()


term_document_list = {}
term_content = {}


def populate_term_document_list(tokens, filename):
    for token in tokens:
        if token in term_document_list:
            if filename in term_document_list[token]:
                document_count = term_document_list[token][filename]
                term_document_list[token][filename] = document_count + 1
            else:
                term_document_list[token][filename] = 1
        else:
            term_document_list[token] = {filename: 1}


def process_document():
    directory_path = "/Users/praneeth.lakmala/Desktop/Material/Parul/2001_txt/"
    files_list = os.listdir(directory_path)
    file_counter = 0
    term_document_list.clear()
    term_content.clear()
    for file_name in files_list:
        if ".txt" not in file_name:
            continue
        file_counter += 1
        if file_counter <= 2000:
            file_handler = open(directory_path + file_name)
            file_content = file_handler.read()
            term_content[file_name] = file_content
            tokens = file_content.split(" ")
            populate_term_document_list(tokens, file_name)


def home(request):
    now = current_time()
    process_document()
    temp = get_template('homepage.html')
    html = temp.render(Context({'current_date': now}))
    return HttpResponse(html)


def search(request):
    print "request : " + str(request.GET)
    if 'q' in request.GET:
        value = request.GET['q']
        files_list = {}
        result_metadata = []
        if value in term_document_list:
            files_list = term_document_list[value]
            # lets check two document
            counter = 0
            for file_name in files_list:
                result_metadata.append((value, file_name, files_list[file_name], term_content[file_name]))
        result_metadata = sorted(result_metadata, key=itemgetter(2), reverse=True)
        temp = get_template('homepage.html')
        now = current_time()
        html = temp.render(Context({'current_date': now, 'files_list': files_list, 'value': value,
                                    'result_metadata': result_metadata}))
        return HttpResponse(html)
