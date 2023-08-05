
export interface FunctionDocumentationObject {
    function: string;
    description: string;
    examples?: (string)[] | null;
    syntax: string;
    syntax_elements?: (SyntaxElementsEntity)[] | null;
}

export interface SyntaxElementsEntity {
    element: string;
    description: string;
}

export const functionDocumentationObjects: FunctionDocumentationObject[] = [{"function": "ABS", "description": "Returns the absolute value of the passed number or series.", "examples": ["ABS(-1.3)", "ABS(A)"], "syntax": "ABS(value)", "syntax_elements": [{"element": "value", "description": "The value or series to take the absolute value of."}]}, {"function": "AND", "description": "Returns True if all of the provided arguments are True, and False if any of the provided arguments are False.", "examples": ["AND(True, False)", "AND(Nums > 100, Nums < 200)", "AND(Pay > 10, Pay < 20, Status == 'active')"], "syntax": "AND(boolean_condition1, [boolean_condition2, ...])", "syntax_elements": [{"element": "boolean_condition1", "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."}, {"element": "boolean_condition2 ... [OPTIONAL]", "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."}]}, {"function": "AVG", "description": "Returns the numerical mean value of the passed numbers and series.", "examples": ["AVG(1, 2)", "AVG(A, B)", "AVG(A, 2)"], "syntax": "AVG(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or series to consider when calculating the average."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or series to consider when calculating the average."}]}, {"function": "BOOL", "description": "Converts the passed arguments to boolean values, either True or False. For numberic values, 0 converts to False while all other values convert to True.", "examples": ["BOOL(Amount_Payed)", "AND(BOOL(Amount_Payed), Is_Paying)"], "syntax": "BOOL(series)", "syntax_elements": [{"element": "series", "description": "An series to convert to boolean values, either True or False."}]}, {"function": "CLEAN", "description": "Returns the text with the non-printable ASCII characters removed.", "examples": ["CLEAN('ABC\n')"], "syntax": "CLEAN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose non-printable characters are to be removed."}]}, {"function": "CONCAT", "description": "Returns the passed strings and series appended together.", "examples": ["CONCAT('Bite', 'the bullet')", "CONCAT(A, B)"], "syntax": "CONCAT(string1, [string2, ...])", "syntax_elements": [{"element": "string1", "description": "The first string or series."}, {"element": "string2, ... [OPTIONAL]", "description": "Additional strings or series to append in sequence."}]}, {"function": "CORR", "description": "Computes the correlation between two series, excluding missing values.", "examples": ["=CORR(A, B)", "=CORR(B, A)"], "syntax": "CORR(series_one, series_two)", "syntax_elements": [{"element": "series_one", "description": "The number series to convert to calculate the correlation."}, {"element": "series_two", "description": "The number series to convert to calculate the correlation."}]}, {"function": "DATEVALUE", "description": "Converts a given string to a date series.", "examples": ["DATEVALUE(A)", "DATEVALUE('2012-12-22')"], "syntax": "DATEVALUE(date_string)", "syntax_elements": [{"element": "date_string", "description": "The date string to turn into a date object."}]}, {"function": "DAY", "description": "Returns the day of the month that a specific date falls on, as a number.", "examples": ["DAY(A)", "DAY('2012-12-22')"], "syntax": "DAY(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the day of."}]}, {"function": "FILLNAN", "description": "Replaces the NaN values in the series with the replacement value.", "examples": ["FILLNAN(A, 10)", "FILLNAN(A, 'replacement')"], "syntax": "FILLNAN(series, replacement)", "syntax_elements": [{"element": "series", "description": "The series to replace the NaN values in."}, {"element": "replacement", "description": "A string, number, or date to replace the NaNs with."}]}, {"function": "FIND", "description": "Returns the position at which a string is first found within text, case-sensitive. Returns 0 if not found.", "examples": ["FIND(A, 'Jack')", "FIND('Ben has a friend Jack', 'Jack')"], "syntax": "FIND(text_to_search, search_for)", "syntax_elements": [{"element": "text_to_search", "description": "The text or series to search for the first occurrence of search_for."}, {"element": "search_for", "description": "The string to look for within text_to_search."}]}, {"function": "IF", "description": "Returns one value if the condition is True. Returns the other value if the conditon is False.", "examples": ["IF(Status == 'success', 1, 0)", "IF(Nums > 100, 100, Nums)", "IF(AND(Grade >= .6, Status == 'active'), 'pass', 'fail')"], "syntax": "IF(boolean_condition, value_if_true, value_if_false)", "syntax_elements": [{"element": "boolean_condition", "description": "An expression or series that returns True or False values. Valid conditions for comparison include ==, !=, >, <, >=, <=."}, {"element": "value_if_true", "description": "The value the function returns if condition is True."}, {"element": "value_if_false", "description": "The value the function returns if condition is False."}]}, {"function": "KURT", "description": "Computes the unbiased kurtosis, a measure of tailedness, of a series, excluding missing values.", "examples": ["=KURT(A)", "=KURT(A * B)"], "syntax": "KURT(series)", "syntax_elements": [{"element": "series", "description": "The series to calculate the unbiased kurtosis of."}]}, {"function": "LEFT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["LEFT(A, 2)", "LEFT('The first character!')"], "syntax": "LEFT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the left portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the start of string."}]}, {"function": "LEN", "description": "Returns the length of a string.", "examples": ["LEN(A)", "LEN('This is 21 characters')"], "syntax": "LEN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose length will be returned."}]}, {"function": "LOWER", "description": "Converts a given string to lowercase.", "examples": ["=LOWER('ABC')", "=LOWER(A)", "=LOWER('Nate Rush')"], "syntax": "LOWER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to lowercase."}]}, {"function": "MAX", "description": "Returns the maximum value among the passed arguments.", "examples": ["MAX(10, 11)", "MAX(Old_Data, New_Data)"], "syntax": "MAX(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or column to consider for the maximum value."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or columns to compute the maximum value from."}]}, {"function": "MID", "description": "Returns a segment of a string.", "examples": ["MID(A, 2, 2)", "MID('Some middle characters!', 3, 4)"], "syntax": "MID(string, starting_at, extract_length)", "syntax_elements": [{"element": "string", "description": "The string or series to extract the segment from."}, {"element": "starting_at", "description": "The index from the left of string from which to begin extracting."}, {"element": "extract_length", "description": "The length of the segment to extract."}]}, {"function": "MIN", "description": "Returns the minimum value among the passed arguments.", "examples": ["MIN(10, 11)", "MIN(Old_Data, New_Data)"], "syntax": "MIN(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or column to consider for the minumum value."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or columns to compute the minumum value from."}]}, {"function": "MONTH", "description": "Returns the month that a specific date falls in, as a number.", "examples": ["MONTH(A)", "MONTH('2012-12-22')"], "syntax": "MONTH(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the month of."}]}, {"function": "MULTIPLY", "description": "Returns the product of two numbers.", "examples": ["MULTIPLY(2,3)", "MULTIPLY(A,3)"], "syntax": "MULTIPLY(factor1, [factor2, ...])", "syntax_elements": [{"element": "factor1", "description": "The first number to multiply."}, {"element": "factor2, ... [OPTIONAL]", "description": "Additional numbers or series to multiply."}]}, {"function": "OFFSET", "description": "Shifts the given series by the given offset. Use a negative offset to reference a previous row, and a offset number to reference a later row.", "examples": ["OFFSET(Nums, 10)", "OFFSET(call_time, -1)"], "syntax": "OFFSET(series, offset)", "syntax_elements": [{"element": "series", "description": "The series to shift up or down."}, {"element": "offset", "description": "An integer amount to shift. Use a negative number to reference a previous row, and a positive number to reference a later row."}]}, {"function": "OR", "description": "Returns True if any of the provided arguments are True, and False if all of the provided arguments are False.", "examples": ["OR(True, False)", "OR(Status == 'success', Status == 'pass', Status == 'passed')"], "syntax": "OR(boolean_condition1, [boolean_condition2, ...])", "syntax_elements": [{"element": "boolean_condition1", "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."}, {"element": "boolean_condition2 ... [OPTIONAL]", "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."}]}, {"function": "POWER", "description": "The POWER function can be used to raise a number to a given power.", "examples": ["POWER(4, 1/2)", "POWER(Dose, 2)"], "syntax": "POWER(value, exponent)", "syntax_elements": [{"element": "value", "description": "Number to raise to a power."}, {"element": "exponent", "description": "The number to raise value to."}]}, {"function": "PROPER", "description": "Capitalizes the first letter of each word in a specified string.", "examples": ["=PROPER('nate nush')", "=PROPER(A)"], "syntax": "PROPER(string)", "syntax_elements": [{"element": "string", "description": "The value or series to convert to convert to proper case."}]}, {"function": "RIGHT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["RIGHT(A, 2)", "RIGHT('The last character!')"], "syntax": "RIGHT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the right portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the end of string."}]}, {"function": "ROUND", "description": "Rounds a number to a given number of decimals.", "examples": ["ROUND(1.3)", "ROUND(A, 2)"], "syntax": "ROUND(value, [decimals])", "syntax_elements": [{"element": "value", "description": "The value or series to round."}, {"element": "decimals", "description": " The number of decimals to round to. Default is 0."}]}, {"function": "SKEW", "description": "Computes the skew of a series, excluding missing values.", "examples": ["=SKEW(A)", "=SKEW(A * B)"], "syntax": "SKEW(series)", "syntax_elements": [{"element": "series", "description": "The series to calculate the skew of."}]}, {"function": "STDEV", "description": "Computes the standard deviation of a series, excluding missing values.", "examples": ["=STDEV(A)", "=STDEV(A * B)"], "syntax": "STDEV(series)", "syntax_elements": [{"element": "series", "description": "The series to calculate the standard deviation of."}]}, {"function": "SUBSTITUTE", "description": "Replaces existing text with new text in a string.", "examples": ["SUBSTITUTE('Better great than never', 'great', 'late')", "SUBSTITUTE(A, 'dog', 'cat')"], "syntax": "SUBSTITUTE(text_to_search, search_for, replace_with, [count])", "syntax_elements": [{"element": "text_to_search", "description": "The text within which to search and replace."}, {"element": "search_for", "description": " The string to search for within text_to_search."}, {"element": "replace_with", "description": "The string that will replace search_for."}, {"element": "count", "description": "The number of times to perform the substitute. Default is all."}]}, {"function": "SUM", "description": "Returns the sum of the given numbers and series.", "examples": ["SUM(10, 11)", "SUM(A, B, D, F)", "SUM(A, B, D, F)"], "syntax": "SUM(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or column to add together."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or columns to sum."}]}, {"function": "TEXT", "description": "Turns the passed series into a string.", "examples": ["=TEXT(Product_Number)", "=TEXT(Start_Date)"], "syntax": "TEXT(series)", "syntax_elements": [{"element": "series", "description": "The series to convert to a string."}]}, {"function": "TRIM", "description": "Returns a string with the leading and trailing whitespace removed.", "examples": ["=TRIM('  ABC')", "=TRIM('  ABC  ')", "=TRIM(A)"], "syntax": "TRIM(string)", "syntax_elements": [{"element": "string", "description": "The value or series to remove the leading and trailing whitespace from."}]}, {"function": "TYPE", "description": "Returns the type of each element of the passed series. Return values are 'number', 'str', 'bool', 'datetime', 'object', or 'NaN'.", "examples": ["TYPE(Nums_and_Strings)", "IF(TYPE(Account_Numbers) != 'NaN', Account_Numbers, 0)"], "syntax": "TYPE(series)", "syntax_elements": [{"element": "series", "description": "The series to get the type of each element of."}]}, {"function": "UPPER", "description": "Converts a given string to uppercase.", "examples": ["=UPPER('abc')", "=UPPER(A)", "=UPPER('Nate Rush')"], "syntax": "UPPER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to uppercase."}]}, {"function": "VALUE", "description": "Converts a string series to a number series. Any values that fail to convert will return an NaN.", "examples": ["=VALUE(A)", "=VALUE('123')"], "syntax": "VALUE(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to a number."}]}, {"function": "VAR", "description": "Computes the variance of a series, excluding missing values.", "examples": ["=VAR(A)", "=VAR(A - B)"], "syntax": "VAR(series)", "syntax_elements": [{"element": "series", "description": "The series to calculate the variance of."}]}, {"function": "WEEKDAY", "description": "Returns the day of the week that a specific date falls on. 1-7 corresponds to Monday-Sunday.", "examples": ["WEEKDAY(A)", "WEEKDAY('2012-12-22')"], "syntax": "WEEKDAY(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the weekday of."}]}, {"function": "YEAR", "description": "Returns the day of the year that a specific date falls in, as a number.", "examples": ["YEAR(A)", "YEAR('2012-12-22')"], "syntax": "YEAR(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the month of."}]}]