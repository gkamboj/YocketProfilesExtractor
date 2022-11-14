from GoogleSheetsUtil import GoogleSheetsUtil
from ProfileDetail import ProfileDetail
from ProfilesListingPage import ProfilesListingPage
from YocketUtil import YocketUtil

if __name__ == '__main__':
    ProfilesListingPage().process_request()
    #print(ProfileDetail().process_shortlisting_request('d32ff6ea-4b00-40af-a0e3-b2739234e9b3').json())