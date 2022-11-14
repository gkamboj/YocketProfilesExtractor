import requests

from ProfileDetail import ProfileDetail
from YocketUtil import YocketUtil
import math


class ProfilesListingPage:

    def get_params(self, config, page):
        params = {
            'page': page,
            'items': int(config['PLP_PAGE_SIZE'][0]),
            'university_id': config['PLP_UNIVERSITY_ID'][0],
            'country_id': int(config['PLP_COUNTRY_ID'][0]),
            'level': int(config['PLP_LEVEL'][0])
        }

        if int(config['PLP_APPLY_YEAR_FILTER'][0]) == 1:
            params['year'] = int(config['PLP_YEAR'][0])

        if int(config['PLP_APPLY_TERM_FILTER'][0]) == 1:
            params['term'] = config[config['PLP_TERM_STRING'][0] + config['PLP_TERM_ACTIVE_FILTER'][0]][0]

        if int(config['PLP_APPLY_COURSE_FILTER'][0]) == 1:
            params['course_taxonomy_id'] = int(config['PLP_COURSE_ID'][0])

        application_status_string = config['APPLICATION_STATUS_STRING'][0]
        application_statuses_to_check_string = config['APPLICATION_STATUSES_TO_CHECK'][0]
        application_statuses_to_check = application_statuses_to_check_string.split(',')
        application_status = ''
        for status in application_statuses_to_check:
            application_status += config[application_status_string + status][0] + ','
        params['application_status'] = application_status[:-1]

        return params

    def process_request(self):
        config = YocketUtil.get_app_config()
        credentials = YocketUtil.get_cred_config()

        url, uuid = config['PLP_URL'][0], credentials['ACCOUNT_UUID'][0]
        is_count_available, request_count, page, max_request_count = False, 1, 0, -1
        gre_max_score, gre_min_score, max_cgpa, min_cgpa = int(config['MAX_GRE_SCORE'][0]), int(config['MIN_GRE_SCORE'][0]), float(config['MAX_CGPA'][0]), float(config['MIN_CGPA'][0])

        params, headers = self.get_params(config, page), YocketUtil.get_headers()

        count, application_status_rejected = 0, config['APPLICATION_STATUS_REJECTED'][0]
        apply_course_filter, desired_course = int(config['PLP_APPLY_COURSE_FILTER'][0]), config['DEFAULT_DESIRED_COURSE'][0]

        while (not is_count_available) or (request_count <= max_request_count):

            response = requests.get(url + uuid, params=params, headers=headers)
            if response.json()['state'] and response.json()['data'] and response.json()['data']['results']:

                if not is_count_available:
                    total = int(response.json()['data']['total'])
                    max_request_count = math.ceil(total / params['items'])
                    is_count_available = True

                for result in response.json()['data']['results']:
                    count += 1
                    username = result['username']
                    university_data = result['university_applications'][0] if result['university_applications'][0] else None

                    is_rejected_applications_request = True if str(university_data['application_status']) == application_status_rejected else False

                    if count >= int(config['PLP_SKIP_RESULTS_COUNT'][0]) and (apply_course_filter or not desired_course or (university_data and desired_course in str(university_data['course_name']).lower())):
                        if result['user_test_scores']:
                            for score in result['user_test_scores']:
                                if score['name'] == 'GRE' and score['composite'] and gre_max_score >= score['composite'] >= gre_min_score:
                                    ProfileDetail.process_detail_request(username, max_cgpa, min_cgpa, is_rejected_applications_request, university_data)
                                    break
                        else:
                            ProfileDetail.process_detail_request(username, max_cgpa, min_cgpa, is_rejected_applications_request, university_data)
                    print("{} profiles done out of {}".format(count, total))

                params['page'] = request_count
                request_count += 1

            else:
                print("No results found for the university")
                break
