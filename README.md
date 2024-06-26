# MockMeister - _Your data generation companion_
MockMeister is a GUI mock (fake) data generation software written in Python.

### Features

<img align="right" width="460" height="250" src="https://github.com/MinaBasem/MockMeister/assets/42482261/ab129d98-38ec-4adc-8659-00b63797f6a9">

- **Interactive Interface:** User-friendly buttons and visual elements enhance the experience.
- **Specifying Data Fields:** Select the desired data points from a pre-defined list (e.g., first name, email address, phone number, address components).
- **Setting Row Count:** Determine the number of data rows to be generated.
- **Generating Data:** Initiate the data generation process using the API and populate the table.
- **Data Export:** Export generated data to CSV.


# Getting Started


### Prerequisites:

- Python 3.x
- PyQt5 library (installation: `pip install PyQt5`)
- requests library (installation: `pip install requests`)
- pandas library (installation: `pip install pandas`)
  
Clone or Download the Repository:
Use Git to clone the repository or download the code files directly.

### Run the Application:
Navigate to the project directory in your terminal and execute:

#### Bash
```
python main.py
```

### Technical Overview

The application leverages the requests library to fetch data from <href>https://random-data-api.com</href>'s API. The retrieved JSON response is parsed using pandas to create a DataFrame. User-selected data fields are then extracted and used to populate a table for visual representation.

### Future Enhancements

- **Data Validation**: Ensure consistency and accuracy of the generated data, especially for specific fields or formats.
- **Advanced Data Generation**: Integrating more capable random data generation algorithms to offer greater control over data types, ranges, and distributions.

### Contribution

We welcome contributions to this project! Feel free to fork the repository, make your changes, and submit a pull request.
