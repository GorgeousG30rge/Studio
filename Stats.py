
class Stats:
    def __init__(self, company):
        self.reporting_company = company

    def show_design_results(self):
        print('Design Dept')
        self.reporting_company.__design.get_test_results()
        print()
    
    def show_front_results(self):
        print('Front Dept')
        self.reporting_company.__front.get_test_results()
        print()

    def show_back_results(self):
        print('Back Dept')
        self.reporting_company.__back.get_test_results()
        print()

    def show_design_totals(self):
        print('Design Dept')
        self.reporting_company.__design.get_totals()
        print()
    
    def show_front_totals(self):
        print('Front Dept')
        self.reporting_company.__front.get_totals()
        print()

    def show_back_totals(self):
        print('Back Dept')
        self.reporting_company.__back.get_totals()
        print()
