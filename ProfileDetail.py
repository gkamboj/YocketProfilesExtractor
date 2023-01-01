import requests

from GoogleSheetsUtil import GoogleSheetsUtil
from YocketUtil import YocketUtil


class ProfileDetail:

    @staticmethod
    def process_detail_request(username, max_cgpa, min_cgpa, is_rejected_applications_request, university_data):
        config = YocketUtil.get_app_config()
        url = config['PDP_URL'][0]
        headers = YocketUtil.get_headers()
        response = requests.get(url + username, headers=headers)
        if response.json()['state'] and response.json()['data'] and response.json()['data']['user_education']:
            data = response.json()['data']
            for education in data['user_education']:
                try:
                    score_type = education['score_type']
                    score = float(education['score'])
                    if (score_type == 'cgpa' and min_cgpa <= score < max_cgpa) or (score_type == 'percent' and score < max_cgpa * 10):
                        print('in process_detail_request - ' + username)
                        shortlisting_data = ProfileDetail.process_shortlisting_request(data['uuid'])
                        GoogleSheetsUtil.add_profile_data_to_sheet(data, shortlisting_data)
                        if is_rejected_applications_request and university_data:
                            GoogleSheetsUtil.add_reject_profile_data_to_sheet(data, university_data)
                    else:
                        print('Score of ' + username + ' - ' + str(score))
                except Exception as ex:
                    print("Exception in process_detail_request for user " + username + ': ' + str(ex))

    @staticmethod
    def process_shortlisting_request(uuid):
        config = YocketUtil.get_app_config()
        url = config['PROFILE_APPLICATIONS_URL'][0]
        headers = YocketUtil.get_headers()
        response = requests.get(url + uuid, headers=headers)
        return response.json()['data'][0]
