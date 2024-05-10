# Importings
import pandas as pd
import numpy as np
import requests
from converter.pgn_data import PGNData
from datetime import datetime
import sys
import os
from dateutil import tz


# Lichess Class
class LichessAPI:
    """
    A class that extract chess games from Lichess.org using the lichess api
    
    ...
    
    Attributes
    ----------
    username : str
        Lichess username
        
    Methods
    -------
    to_pgn()
        Extracts the chess games and exports them into a PGN (Portable Game Notation) file.
        
    to_csv()
        Extracts the chess games and exports them into a PGN and two CSV (Comma-Separated Values) files,
        the first file is for games info and the second file is for moves info.
    
    to_dataframe()
        Extracts the chess games and exports them into a PGN and two CSV files and then reads the games info 
        csv file into a dataframe.
    """
    
    def __init__(self,username):
        """
        Parameters
        ----------
        username : str
            Lichess username
        """
        self.username = username
        
        # Lichess API
        self.url = f"https://lichess.org/api/games/user/{self.username}?tags=true&clocks=true&evals=true&opening=true"
        # Current Date
        now = datetime.now().strftime("%Y-%m-%dT%H.%M.%S")
        # Filename without the PGN extension
        self.filename = f"{now}-{self.username}.pgn"
        # Filename with the PGN extension
        self.filepath = os.path.join("data",f"{self.filename}")
        
        
        
    def to_pgn(self):
        """
        Extracts the chess games and exports them into a PGN (Portable Game Notation) file.
            
        """
        # Extracting the data from the lichess api and export it to a pgn file
        with open(self.filepath,"wb") as f:
            response = requests.get(self.url,stream=True)
            if response.status_code == 200:
                f.write(response.content)
            else:
                raise Exception(f"Username '{self.username}' doesn't exist.")

            
    def to_csv(self):
        """
        Extracts the chess games and exports them into a PGN and two CSV (Comma-Separated Values) files,
        the first file is for games info and the second file is for moves info.
            
        """
        # Call the to_pgn method if it's not called before
        if self.filename not in os.listdir("data"):
            self.to_pgn()
        
        # Converting the PGN file to two csv files, one for games info and the other for moves
        os.chdir("data")
        pgn_data = PGNData(self.filename)
        result = pgn_data.export()
        os.chdir("../")
        
    def to_dataframe(self):
        """
        Extracts the chess games and exports them into a PGN and two CSV files and then reads the games info 
        csv file into a dataframe.

        Returns
        -------
        DataFrame
            A pandas DataFrame of the games info csv file
        
        """
        
        # Remove the .pgn from the filename
        filename = self.filename[:-4]
        csv_file = f"{filename}_game_info.csv"
        
        # Call the to_csv file if it's not called before
        if csv_file not in os.listdir("data"):
            self.to_csv()
        
        # Reading the games info csv file into a pandas DataFrame
        filepath = os.path.join("data",csv_file)
        df = pd.read_csv(filepath)
        return df
    
    
# Data Wrangling class
class Wrangle:
    """
    A class that cleans the chess games info DataFrame for analysis.
    
    ...
    
    Attributes
    -----------
    df : DataFrame
        The DataFrame that contains the chess games info
        
    Methods
    -------
    wrangle(time_zone="Egypt/Cairo")
        Cleans the data from analysis and visualizations

    """
    
    def __init__(self,df,username,timezone):
        """
        Parameters
        ----------
        df : DataFrame
            The DataFrame that contains the chess games info
            
        username : String
            Lichess username
            
        timezone : str
            A string of the local timezone
        """
        self.df = df
        self.username = username
        self.timzone = timezone
        
    def __utc_to_localtime(self,utcdatetime,time_zone='Egypt/Cairo'):
        """
        Converts the UTC datetime to Cairo datetime
        
        If argument 'time_zone' isn't passed in, the default timezone is "Egypt/Cairo"
        
        Parameters
        ----------
        utcdatetime : str
            A utc datetime string in this format '%Y.%m.%d %H:%M:%S'
            
        Returns
        -------
        Datetime
            A datetime in the timezone specified
        """
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(time_zone)
        utc = datetime.strptime(utcdatetime, '%Y.%m.%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        return local
    
    def __chess_type(self,time_control):
        """
        This function takes the time control and return the chess game type

        Parameters
        ----------
        time_control : str
            the time control of the game

        Returns
        -------
        Str
            the chess game type
        """
        # "-" indicates that the game had no time control
        if time_control == '-':
            return "Classical"

        # Extracting the seconds from the string
        plus_index = time_control.index("+")
        seconds = int(time_control[:plus_index])

        if seconds in range(0,30):
            return "UltraBullet"

        if seconds in range(30,180):
            return "Bullet"

        if seconds in range(180,600):
            return "Blitz"

        if seconds in range(600,1800):
            return "Rapid"

        if seconds >= 1800:
            return "Classical"
        
    
class Wrangle:
    """
    A class that cleans the chess games info DataFrame for analysis or time series forcast.
    
    ...
    
    Attributes
    -----------
    df : DataFrame
        The DataFrame that contains the chess games info
        
    Methods
    -------
    for_analysis()
        Cleans the data from analysis and visualizations
        
    fo_time_series()
        Cleans the data from time series forecast
    """
    
    def __init__(self,df,username,timezone):
        """
        Parameters
        ----------
        df : DataFrame
            The DataFrame that contains the chess games info
            
        username : Str
            Lichess username
        
        timezone : str
            A string of the local timezone
        """
        self.df = df
        self.username = username
        self.timezone = timezone
        
    def __utc_to_localtime(self,utcdatetime,time_zone='Egypt/Cairo'):
        """
        Converts the UTC datetime to Cairo datetime
        
        If argument 'time_zone' isn't passed in, the default timezone is "Egypt/Cairo"
        
        Parameters
        ----------
        utcdatetime : str
            A utc datetime string in this format '%Y.%m.%d %H:%M:%S'
            
        Returns
        -------
        Datetime
            A datetime in the timezone specified
        """
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(time_zone)
        utc = datetime.strptime(utcdatetime, '%Y.%m.%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        return local
    
    def __chess_type(self,time_control):
        """
        This function takes the time control and return the chess game type

        Parameters
        ----------
        time_control : str
            the time control of the game

        Returns
        -------
        Str
            the chess game type
        """
        # "-" indicates that the game had no time control
        if time_control == '-':
            return "Classical"

        # Extracting the seconds from the string
        plus_index = time_control.index("+")
        seconds = int(time_control[:plus_index])

        if seconds in range(0,30):
            return "UltraBullet"

        if seconds in range(30,180):
            return "Bullet"

        if seconds in range(180,600):
            return "Blitz"

        if seconds in range(600,1800):
            return "Rapid"

        if seconds >= 1800:
            return "Classical"
        
    
    def wrangle(self):
        """
        This method cleans the DataFrame from analysis and visualizations
            
        Returns
        -------
        DataFrame
            A clean DataFrame that is ready for analysis and visualizations
        """
        
        # Read the openings csv file
        openings = pd.read_csv("../data/Chess Opening Reference - Sheet1.csv")

        # Columns to drop
        columns_to_drop = ['game_order','round','ply_count','file_name','date_played','utc_date','utc_time','date_created',
                           'datetime_utc','datetime_cairo','white','black','winner','winner_elo','loser','loser_elo','winner_loser_elo_diff',
                           'event','white_elo','black_elo','white_rating_diff','black_rating_diff','white_title','black_title','eco']

        # Games types
        self.df['game_type'] = self.df['event'].apply(lambda x:'Casual' if "Casual" in x else 'Rated')
        self.df['chess_type'] = self.df['time_control'].apply(lambda x: self.__chess_type(x))
        self.df['in_tournament'] = self.df['event'].apply(lambda x:0 if 'game' in x else 1)

        # Fill the nulls
        to_fill = {"white_rating_diff":"0","black_rating_diff":"0",
                   "white_title":"None","black_title":"None"}
        self.df.fillna(to_fill,inplace=True)

        # Colors and Usernames
        self.df['color'] = self.df.apply(lambda x:'white' if x.white == self.username else "black",axis=1)
        self.df['opponent_username'] = self.df.apply(lambda x:x.white if x.color == 'black' else x.black,axis=1)
        self.df['opponent_title'] = self.df.apply(lambda x:x.white_title if x.color == 'black' else x.black_title,axis=1)

        # Elo and ratings
        mask_1 = self.df['white_elo'] != '?'
        mask_2 = self.df['black_elo'] != "?"
        self.df = self.df[mask_1 & mask_2]
        self.df['my_elo'] = self.df.apply(lambda x:x.white_elo if x.color == 'white' else x.black_elo,axis=1).astype(int)
        self.df['opponent_elo'] = self.df.apply(lambda x:x.black_elo if x.color == 'white' else x.white_elo,axis=1).astype(int)
        self.df['elo_diff'] = self.df['my_elo'].astype(int) - self.df['opponent_elo'].astype(int)
        self.df[['white_rating_diff','black_rating_diff']] = self.df[['white_rating_diff','black_rating_diff']].astype(int) 
        self.df['rating_gained'] = self.df.apply(lambda x:x.white_rating_diff if x.white_rating_diff > 0 and x.color == 'white' else
                                      (x.black_rating_diff if x.black_rating_diff > 0 and x.color == 'black' else 0),axis=1)
        self.df['rating_lost'] = self.df.apply(lambda x:-(x.white_rating_diff) if x.white_rating_diff < 0 and x.color == 'white' else
                                      (-(x.black_rating_diff) if x.black_rating_diff < 0 and x.color == 'black' else 0),axis=1)

        # Games result and opening
        self.df['result'] = self.df.apply(lambda x:'win' if x.winner == self.username else ('loss' if x.loser == self.username else 'draw'),axis=1)
        self.df['opening'] = self.df['eco'].apply(lambda x:openings[openings['ECO Code'] == x]['Name'].values[0] if x != "?" else "Unknown")
        
        # Date and time
        self.df['datetime_utc'] = self.df['utc_date'] + " " + self.df['utc_time']
        self.df['datetime_cairo'] = self.df['datetime_utc'].apply(lambda x:self.__utc_to_localtime(x,time_zone=self.timezone))
        self.df['date'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%D"))
        self.df['year'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%Y"))
        self.df['month'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%b"))
        self.df['day'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%d"))
        self.df['day_of_week'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%A"))
        self.df['hour'] = self.df['datetime_cairo'].apply(lambda x:x.strftime("%H"))
        self.df['date'] = self.df['date'].astype(np.datetime64)

        # Drop the unnecessary columns
        self.df.drop(columns_to_drop,axis=1,inplace=True)
        
        # Reset the game_id column
        self.df['game_id'] = np.arange(0,self.df.shape[0])

        return self.df