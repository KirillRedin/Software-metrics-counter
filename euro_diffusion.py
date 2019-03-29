from country import Country


class EuroDiffusion:
    def __init__(self):
        self.grid = []
        self.countries = []
        self.errors = []
        self.cases_count = 0
        self.countries_amount = 0
        self.days = 0
        self.case_is_correct = True

        # Variables for dynamic grid creation
        self.grid_length, self.grid_height = 0, 0

    def parse(self, name):
        file = open(name, 'r')
        country_number = 0
        line_number = 0
        case_is_started = False

        for line in file:
            line_number += 1
            # Skip whitespaces
            if not line.strip():
                continue
            # If new case is started we are reading line with country parameters
            if case_is_started:
                country_number += 1

                # If current case has no Errors split current line, otherwise skip it until case is ended
                if self.case_is_correct:
                    args = line.split()

                    # Check if current line has no mistakes
                    if self.line_is_correct(args, line_number):
                        xl, yl, xh, yh = int(args[1]), int(args[2]), int(args[3]), int(args[4])

                        # Create country using line arguments
                        country = Country(args[0], xl, yl, xh, yh)

                        # Update values for grid size
                        self.grid_length = max(self.grid_length, xl + 1, xh + 1)
                        self.grid_height = max(self.grid_height, yl + 1, yh + 1)

                        self.countries.append(country)

                # Check if we read given number of lines
                if country_number == self.countries_amount:
                    # End current case
                    case_is_started = False

            else:
                # Check if we ended reading case or it's just the beginning of file
                if self.cases_count > 0:

                    # Check if last case have no Errors and put cities on grid
                    if self.case_is_correct:
                        self.fill_grid()

                        # Check on Errors after filling and enter main counting loop
                        if self.case_is_correct:
                            self.count_days()

                    self.print_results()

                    # Reset variables for next case
                    self.clear_variables()

                try:
                    country_number = 0
                    self.cases_count += 1

                    # Get number of countries for next case
                    self.countries_amount = int(line)

                    # Check if end of cases were found
                    if self.countries_amount == 0:
                        break
                    elif self.countries_amount < 0:
                        raise ValueError

                    case_is_started = True

                except ValueError:
                    self.errors.append({'case': self.cases_count, 'text': 'UNEXPECTED VALUE IN LINE %s' % line_number})
                    self.case_is_correct = False

    def line_is_correct(self, args, line_number):
        if len(args) != 5:
            self.errors.append({'case': self.cases_count, 'text': 'ARGS AMOUNT ERROR IN LINE %s' % line_number})
            self.case_is_correct = False
            return False
        else:
            # Check if country name is correct
            if not args[0].isalpha():
                self.errors.append({'case': self.cases_count,
                                    'text': 'COUNTRY NAME MUST INCLUDE ONLY ALPHABETIC CHARACTERS. LINE %s' % line_number})
                self.case_is_correct = False
                return False
            elif len(args[0]) > 25:
                self.errors.append({'case': self.cases_count,
                                    'text': 'COUNTRY NAME CAN NOT CONSIST MORE THAN 25 CHARACTERS. LINE %s' % line_number})
                self.case_is_correct = False
                return False

            # Check if country coordinates are correct
            for i in range(1, 5):
                try:
                    if int(args[i]) < 0:
                        self.errors.append({'case': self.cases_count, 'text': 'COORDINATE CANNOT BE NEGATIVE NUMBER %s' % line_number})
                        self.case_is_correct = False
                        return False

                except ValueError:
                    self.errors.append({'case': self.cases_count, 'text': 'UNEXPECTED ARGUMENT VALUE %s' % line_number})
                    self.case_is_correct = False
                    return False
        return True

    def count_days(self):
        # Check if all cities have all motifs
        while not self.is_complete():
            self.days += 1

            for i in range(self.grid_length):
                for j in range(self.grid_height):
                    current_city = self.grid[i][j]

                    if current_city != 0:
                        # For each city prepare coins for transportation
                        current_city.prepare_coins()

            for country in self.countries:
                # Transport prepared coins
                country.transport_coins()

    def countries_are_connected(self, country, country_list):
        # List of countries which can be accessed
        country_list = country_list

        # If current country already in this list, back to higher level, otherwise add country to list
        if country in country_list:
            return
        else:
            country_list.append(country)

        for neighbor in country.neighbors:
            # For country neighbors recursive call to get their neighbors
            self.countries_are_connected(neighbor, country_list)

        # Check if all countries can be accessed
        if len(country_list) == len(self.countries):
            return True

        return False

    def countries_are_unique(self):
        country_names = []

        for country in self.countries:
            if country.name not in country_names:
                country_names.append(country.name)
            else:
                return False

        return True

    def is_complete(self):
        result = True

        for country in self.countries:
            # If at least one country is not complete result always will be False cause F && T == F and T && F == F
            result = country.is_complete(self.countries_amount, self.days) and result

        return result

    def fill_grid(self):
        # Check if all countries have different names
        if not self.countries_are_unique():
            self.errors.append({'case': self.cases_count, 'text': 'COUNTRIES MUST HAVE DIFFERENT NAMES'})
            self.case_is_correct = False
            return

        # Fill grid with 0
        for i in range(self.grid_length):
            cities = []
            for j in range(self.grid_height):
                cities.append(0)
            self.grid.append(cities)

        for country in self.countries:
            for city in country.cities:
                # Check if current cell is not occupied by another city
                if self.grid[city.x][city.y] == 0:
                    self.grid[city.x][city.y] = city
                else:
                    self.errors.append({'case': self.cases_count,
                                        'text': 'MULTIPLE CITIES CAN NOT HAVE SAME COORDINATES'})
                    self.case_is_correct = False
                    return

        # Filling country and city neighbors
        for country in self.countries:
            country.fill_neighbors(self.grid, self.countries)

        # Check if all countries are connected
        if not self.countries_are_connected(self.countries[0], []):
            self.errors.append({'case': self.cases_count, 'text': 'COUNTRIES ARE NOT CONNECTED'})
            self.case_is_correct = False

    def clear_variables(self):
        self.grid = []
        self.countries = []
        self.countries_amount = 0
        self.days = 0
        self.grid_length, self.grid_height = 0, 0
        self.case_is_correct = True

    def print_results(self):
        print('Case %d' % self.cases_count)

        if self.case_is_correct:
            # Sort results by day and name when country became complete
            countries = sorted(self.countries, key=lambda country: (country.complete_day, country.name))

            for country in countries:
                print(country.name, country.complete_day)
        else:
            for error in self.errors:
                if error['case'] == self.cases_count:
                    print('ERROR: %s' % error['text'])

        print()


diffusion_counter = EuroDiffusion()
diffusion_counter.parse('test3')

