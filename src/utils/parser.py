from .form_summary import FormSummary


def parse_form_data(form_name, matches):
    started = False
    form_name = form_name.lower()

    for match in matches:
        titleized_name, title, year = match.text.split('\n')
        name = titleized_name.lower()
        # Non-matches until the first match
        if name != form_name and started == False:
            continue
        # First match
        elif name == form_name and started == False:
            # First accurate result will be the latest year, i.e. maximum year
            form_summary = FormSummary(titleized_name, title, year)
            started = True
        # Subsequent matches
        elif name == form_name and started == True:
            form_summary.update_min_year(year)
        # First non-match after matches (name != form_name and started == True)
        else:
            break
    return form_summary


def parse_range(matches, form_name, start_year, end_year):
    started = False
    pdf_links = []
    form_name = form_name.lower()
    for match in matches:
        name, _, year = match.text.split('\n')
        name = name.lower()
        # non-match until first match
        if name != form_name and started == False:
            continue
        # form_name match but year more recent than selected range
        elif name == form_name and int(year) > int(end_year):
            continue
        # matching form_name and within correct year range
        elif name == form_name and int(year) in range(int(start_year), int(end_year) + 1):
            if started == False:
                started = True
            pdf_links.append(match)
        # First non-match after matches ((name != form_name and started == True) or (name == form_name and year < start_year))
        else:
            break
    return pdf_links
