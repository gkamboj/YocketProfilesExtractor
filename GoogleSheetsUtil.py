import pygsheets
from datetime import datetime

from YocketUtil import YocketUtil


class GoogleSheetsUtil:

    @staticmethod
    def add_profile_data_to_sheet(profile_data, applications_data):
        config = YocketUtil.get_app_config()
        gc = pygsheets.authorize(service_file=config['GOOGLE_SERVICE_ACCOUNT_FILE'][0])

        sheet = gc.open(config['GOOGLE_SHEET_NAME'][0])
        worksheet = sheet[int(config['GOOGLE_SHEET_WORKSHEET'][0])]

        try:
            sheet_data = GoogleSheetsUtil.create_profile_fields(profile_data, config)
        except Exception as e:
            print(
                "Exception while creating profile fields for the the user " + profile_data['username'] + ": " + str(e))
            return

        for application in applications_data['users_university_applications']:
            try:
                cols = worksheet.get_col(1, include_tailing_empty=False)
                last_row = len(cols)
                if application['id'] not in cols:
                    GoogleSheetsUtil.update_application_data(application, sheet_data, config)
                    worksheet.insert_rows(last_row, number=1, values=sheet_data)
            except Exception as ex:
                print("Exception for username {} and unique id {}: ".format(applications_data['username'], application['id']) + str(ex))

    @staticmethod
    def create_profile_fields(profile_data, config):

        profile_url = config['PROFILE_URL'][0] + profile_data['username'].replace(' ', '%20')
        profile_name = profile_data['profile_name']
        name_cell = '=HYPERLINK("' + profile_url + '", "' + profile_name + '")'

        cgpa, percentage, backlogs, ug_college = None, None, None, None
        if profile_data['user_education']:
            for education in profile_data['user_education']:
                score_type = education['score_type']
                if score_type == 'cgpa' or score_type == 'percent':
                    if score_type == 'cgpa':
                        cgpa = education['score']
                    if score_type == 'percent':
                        percentage = education['score']
                    backlogs = education['backlogs']
                    if education['institutes']:
                        ug_college = education['institutes']['name']
                    break

        gre, awa, toefl, ielts = None, None, None, None
        if profile_data['user_test_scores']:
            for test_score in profile_data['user_test_scores']:
                if test_score['name'] == 'GRE':
                    gre = test_score['composite']
                    if test_score['components']:
                        awa = test_score['components']['awa']
                        if isinstance(awa, dict) and 'gre_awa_score' in awa:
                            awa = awa['gre_awa_score']

                elif test_score['name'] == 'TOEFL':
                    toefl = test_score['composite']
                elif test_score['name'] == 'IELTS':
                    ielts = test_score['composite']

        work_experience, technical_papers, projects = None, None, None
        if profile_data['technical_papers']:
            technical_papers = len(profile_data['technical_papers'])
        if profile_data['projects']:
            projects = len(profile_data['projects'])
        if profile_data['work_experiences']:
            total_work_exp = 0
            for exp in profile_data['work_experiences']:
                start_date_str = exp['from_date']
                if start_date_str:
                    start_date = GoogleSheetsUtil.get_date_instance(start_date_str)
                    if not exp['is_working_now']:
                        end_date_str = exp['to_date']
                        if not end_date_str:
                            continue
                        end_date = GoogleSheetsUtil.get_date_instance(end_date_str)
                        delta = end_date - start_date
                    else:
                        delta = GoogleSheetsUtil.get_date_instance(None) - start_date
                    total_work_exp += (delta.days / 365)
            work_experience = round(total_work_exp, 2)

        term, year = str(profile_data['term']).capitalize(), profile_data['year']

        data = [None, name_cell, None, None, None, None, None, cgpa, percentage, backlogs, ug_college, gre, awa, toefl,
                ielts, work_experience, technical_papers, projects, year, term, None, None, None]
        return data

    @staticmethod
    def update_application_data(application_data, sheet_data, config):
        unique_id = application_data['id']
        sheet_data[0] = unique_id

        university_id, university_slug, university_name = str(application_data['university_id']), application_data[
            'slug'], application_data['university_name']
        university_name_cell = GoogleSheetsUtil.get_university_name_cell(university_id, university_slug,
                                                                         university_name, config)
        sheet_data[2] = university_name_cell

        data = application_data['data']
        country, expenses = data['country_name'], None
        if 'pg_living_expense' in data:
            expenses = data['pg_living_expense']

        sheet_data[3], sheet_data[4] = country, expenses

        degree, course, status = application_data['credential'], application_data['university_course_name'], str(
            application_data['application_type']).capitalize()
        sheet_data[5], sheet_data[6], sheet_data[-3] = degree, course, status

        applied_date, decision_date = None, None
        if application_data['applied_date']:
            applied_date = GoogleSheetsUtil.get_date_instance(application_data['applied_date']).strftime(
                config['GOOGLE_SHEET_DATE_FORMAT'][0])
        if application_data['decision_date']:
            decision_date = GoogleSheetsUtil.get_date_instance(application_data['decision_date']).strftime(
                config['GOOGLE_SHEET_DATE_FORMAT'][0])
        sheet_data[-1], sheet_data[-2] = decision_date, applied_date

    @staticmethod
    def get_university_name_cell(university_id, university_slug, university_name, config):
        university_url = config['UNI_PAGE_URL'][0] + university_slug + '-' + university_id
        university_name_cell = '=HYPERLINK("' + university_url + '", "' + university_name + '")'
        return university_name_cell

    @staticmethod
    def get_date_instance(date_string):
        if date_string:
            date_time = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            date_time = datetime.today()
        return date_time

    @staticmethod
    def update_rejected_application_data(university_data, sheet_data, config):
        # university_data = listing_application_data['university_applications'][0]
        university_id = str(university_data['university_id'])

        sheet_data[0] = university_data['student_id'] + '_' + university_id + '_' + str(university_data['university_course_id'])

        university_slug, university_name = university_data['university_slug'], university_data['university_name']
        sheet_data[2] = GoogleSheetsUtil.get_university_name_cell(university_id, university_slug, university_name, config)

        sheet_data[3] = config['GOOGLE_SHEET_DEFAULT_COUNTRY'][0]

        degree, course, status = university_data['credential'], university_data['course_name'], 'Rejected'
        sheet_data[5], sheet_data[6], sheet_data[-3] = degree, course, status

    @staticmethod
    def add_reject_profile_data_to_sheet(profile_data, university_data):
        config = YocketUtil.get_app_config()
        gc = pygsheets.authorize(service_file=config['GOOGLE_SERVICE_ACCOUNT_FILE'][0])

        sheet = gc.open(config['GOOGLE_SHEET_NAME'][0])
        worksheet = sheet[int(config['GOOGLE_SHEET_WORKSHEET'][0])]

        try:
            cols = worksheet.get_col(1, include_tailing_empty=False)
            unique_id = university_data['student_id'] + '_' + str(university_data['university_id']) + '_' + str(university_data['university_course_id'])
            last_row = len(cols)
            if unique_id not in cols:
                sheet_data = GoogleSheetsUtil.create_profile_fields(profile_data, config)
                GoogleSheetsUtil.update_rejected_application_data(university_data, sheet_data, config)
                worksheet.insert_rows(last_row, number=1, values=sheet_data)
        except Exception as ex:
            print("Exception in add_reject_profile_data_to_sheet for username {} and unique id {}: ".format(profile_data['username'], unique_id) + str(ex))
