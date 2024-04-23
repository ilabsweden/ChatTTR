# Chat TTR
Type-Token Ratio calculator for dialogue files. 


## Dependencies

ChatTTR runns under Python 3.3+. Install dependencies by running the following command from a terminal: 

    pip install -r requirements.txt

## Usage

ChatTTR currently reads dialogue log files from [PepperChat](https://github.com/ilabsweden/pepperchat). A log file may be analysed as follows: 

    python ttr.py <path to log file>

Optionally, the analsis can be saved to an excel file:

    python ttr.py <path to log file> --save ttr-analysis.xlsx


## License

This project is released under the MIT license. Please refer to [LICENSE.md](LICENSE.md) for license details.

## Author

Erik Billing, University of Skövde, https://www.his.se/erikb