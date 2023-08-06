""" This module provides fuctions to convert a pdf to text"""


class Converter:
    """A simple converter for converting pdf to text.""" 

    def convert(self,path):
        """
        Convert the given pdf to text.

        Parameters:
        path(str):The path to pdf file. 
        
        Returns:
        str:The content of the pdf file as text.
        """
        print("pdf2text")