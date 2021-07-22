# Welcome To the Power BI Premium and Embedded Tools and Utilities Repository

This repository is meant to host tools and utilities designed to improve all aspects of Power BI capacity managment and lifecycle.

## Amended in this version:
This amendment is for Analysts that use Python as preferred language and Service Principal to authenticate to their environments.
The Python scripts can be found in the  Realistic Tool Folder. They are in fact related ONLY to the Realistic Tool Option of the Load-Test-Tool.

The Python code has been structured following the reasoning behind the original tool in PowerShell but also adding the logic required for the SP authentication method to function.

Note: For the Service Principal Authentication to work, within the .html file, the token type is being set to Embed (tokenType: models.TokenType.Embed). 

It is strongly recommended to read the documentation related to the official Power BI Load Testing Tool to understand better the logic behind the Python code.

### Authors in this Amendment:
Mariangela Rossi https://www.linkedin.com/in/mariangela-rossi-500a139b/ , 
Rajah Iyer https://www.linkedin.com/in/rajah-iyer-628689168/

# Available Tools (as of July 2019)

[Load Testing Tool](http://aka.ms/PowerBILoadTestingTool).

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
