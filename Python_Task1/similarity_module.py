import numpy as np
import pandas as pd
import random
from statistics_module import Calculate_mean

class SimilarityCalculator:
    """
    This is the main class, it calculates the similarity between two input (artists,
    tracks or ids) using metrics (Euclidean, manhattan, cosine and pearson),
    and generate top 5 similar artist and recommendation.
    """
    def __init__(self, data_dict):
        """
        This is a constructor that can take only one parameter, a dictionary with artist as keys
        """
        self.data = data_dict
        self.features = [ "popularity", "speechiness", "tempo", "acousticness", 'danceability', 'energy', 'loudness', 'liveness', 'valence']
        self.artist_index = set(data_dict.keys()) # set all artist name
        self.track_index = set() # populate with track name
        self.id_index = set()  # populate with id

        # Loop thought data dictionary to extract all tracks and IDs
        # Add all name for the track and check if track have an id and add it to index
        for artist, tracks in data_dict.items():
            self.track_index.update(tracks.keys())
            for track_name, features in tracks.items():
                if 'id' in features:
                    self.id_index.add(features['id'])

    def euclidean(self, input1, input2):
        """
        This method takes two parameters and calculate the similarity base on Euclidean distance,
        and return the similarity score. if num1 or num2 is missing it return 0.0.
        """
        num1, num2 = self.similar_feature(input1), self.similar_feature(input2)
        if not num1 or not num2:
            return 0.0
        # Euclidean similarity calculation
        else:
            return 1 / (1 + np.linalg.norm(np.array(num1) - np.array(num2)))

    def cosine(self, input1, input2):
        """
        This method takes two parameters and calculate the similarity base on cosine distance,
        and return the similarity score. if num1 or num2 is missing it return 0.0
        """
        num1, num2 = self.similar_feature(input1), self.similar_feature(input2)
        if not num1 or not num2:
            return 0.0
        # cosine similarity calculation
        # convert to numpy array and calculate the magnitude
        else:
           num1_array, num2_array = np.array(num1), np.array(num2)
           magnitude1, magnitude2 = np.linalg.norm(num1_array), np.linalg.norm(num2_array)
           return np.dot(num1_array, num2_array) / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0.0

    def pearson(self, input1, input2):
        """
        This method takes two parameters and calculate the similarity base on pearson distance,
        and return the similarity score. if num1 or num2 is missing  or length(num1) <1 it returns 0.0
        """
        num1, num2 = self.similar_feature(input1), self.similar_feature(input2)
        if not num1 or not num2 or len(num1) < 2:
            return 0.0
        # pearson similarity calculation
        # convert to numpy array, calculate mean, center the data and calculate the magnitude
        else:
           num1_array, num2_array = np.array(num1), np.array(num2)
           mean1, mean2 = np.mean(num1_array), np.mean(num2_array)
           num1_centered, num2_centered = num1_array - mean1, num2_array - mean2
           magnitude1, magnitude2 = np.linalg.norm(num1_centered), np.linalg.norm(num2_centered)
           return np.dot(num1_centered, num2_centered) / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0.0

    def manhattan(self, input1, input2):
        """
        This method takes two parameters and calculate the similarity base on cosine distance,
        and return the similarity score. if num1 or num2 is missing it return 0.0
        """
        num1, num2 = self.similar_feature(input1), self.similar_feature(input2)
        if not num1 or not num2:
            return 0.0
        # Manhattan similarity calculation
        else:
           return 1 / (1 + np.sum(np.abs(np.array(num1) - np.array(num2))))


    def input_validation(self, input1, input1_type, input2, input2_type, metric='euclidean'):
        """
        This method takes three parameters, it validates input before similarity calculation. it checks:
        1. Both items must exist in the dataset
        2. Cannot compare an item with itself
        3. Cannot compare items of different type
        return the similarity score if input validated, or raise a value error if not.
        """
        # Check if both items exist
        if not self.input_exists(input1, input1_type):
            raise ValueError(f"'{input1}' not found in data file as {input1_type}.")
        if not self.input_exists(input2, input2_type):
            raise ValueError(f"'{input2}' not found in data file as {input2_type}.")
        if input1 == input2 and input1_type == input2_type:
            raise ValueError(f"Cannot compare an item with itself.")
        if input1_type != input2_type:
            raise ValueError(f"Cannot compare items of different types: {input1_type} vs {input2_type}.")
        return self._similarity_score(input1, input2, metric)


    def input_exists(self, inputs, input_type):
        """
        This method takes two parameters, check if input exist in the data file and
        returns Boolean value, True or False
        """
        if input_type == "artist":
            return inputs in self.artist_index
        elif input_type == "track":
            return inputs in self.track_index
        elif input_type == "id":
            return inputs in self.id_index
        return False


    def tracks_similarity(self, track1, track2, metric='euclidean'):
        """This method calculate similarity b/w two tracks and return the score """
        return self._similarity_score(track1, track2, metric)

    def artists_similarity(self, artist1, artist2, metric='euclidean'):
        """This method calculate similarity b/w two artist and returns the score."""
        return self._similarity_score(artist1, artist2, metric)


    def _similarity_score(self, input1, input2, metric='euclidean'):
        """This is a private and a helper method that calculate the similarity score,
        return the result using Euclidean metric as default and raise a value error
        if metric not found """
        all_metrics = {
            'euclidean': self.euclidean,
            'cosine': self.cosine,
            'pearson': self.pearson,
            'manhattan': self.manhattan
        }
        if metric not in all_metrics:
            raise ValueError(f"Invalid metric: {metric}")
        return all_metrics[metric](input1, input2)


    def top5_similar_artist(self, input_name, input_type='artist', metric='euclidean'):
        """
        Get top 5 similar artists or tracks. Only includes artists with similarity > 0.8
        For artists: returns artists 2-6 (skipping the artist itself)
        For tracks: returns tracks 2-6 (skipping the track itself),
        returns list of 5 Artists.
        """
        if input_type not in ['artist', 'track']:
            raise ValueError("input type must be 'artist' or 'track'")

        all_items = self._all_similar(input_type)
        if input_name not in all_items: # check if input exist
            return []                   # return an empty list if it does not exist

        # Calculate similarity with all other items
        similar_items = []
        for other_item in all_items:
            if other_item == input_name: # Skip comparing with itself
                continue
            other_vector = self.similar_feature(other_item)
            if not other_vector:  # Skip artists with similarity ≤ 0.8
                continue
            similarity = self._similarity_score(input_name, other_item, metric)

            if input_type == 'artist' and similarity <= 0.8: # only include if similarity > 0.8
                continue
            similar_items.append([other_item, similarity]) # store input and similarity

        if not similar_items:  # Check if any similar items found
            return []          # return an empty list if no

        # Sort by similarity descending order and return top 5
        similar_file = pd.DataFrame(similar_items, columns=['item', 'similarity'])
        similar_file = similar_file.sort_values('similarity', ascending=False)
        # Return items 2-6 (index 1-5), skipping the item itself which would be first
        return similar_file.iloc[1:6]['item'].tolist()


    def top5_artists_validation(self, artist_name, metric='euclidean'):
        """
        This method takes two parameters and validate them for User interface module to use.
        return the list of top 5 artist, ValueError if artist does not exist or metric is invalid
        """
        if not self.input_exists(artist_name, "artist"):
            raise ValueError(f"Artist '{artist_name}' not found in data file.")
        if metric not in ['euclidean', 'cosine', 'pearson']:  # Check if metric is valid for top 5
            raise ValueError(f"Invalid metric: {metric}. Must be 'euclidean', 'cosine', or 'pearson'")
        # Call the original method
        return self.top5_similar_artist(artist_name, 'artist', metric)


    def recommendations(self, input_name, input_type='artist', metric='cosine', num_recommendations=10):
        """
        This method takes 4 parameters, randomly select 10 artist for recommendation,
        Calculate similarity with all other items, Sort by similarity, Take top 20 and
        Randomly select requested number, return list of 10 recommend items.
        """
        if input_type not in ['artist', 'track']:
            raise ValueError("input type must be 'artist' or 'track'")
        # Get similar items
        similar_items = []
        all_items = self._all_similar(input_type)

        for other_item in all_items:
            if other_item == input_name: # skip the item itself
                continue

            similarity = self._similarity_score(input_name, other_item, metric)
            similar_items.append([other_item, similarity])

        if not similar_items: # check if no similar item
            return []         # return an empty list

        # Sort descending order by similarity
        similar_file = pd.DataFrame(similar_items, columns=['item', 'similarity'])
        similar_file = similar_file.sort_values('similarity', ascending=False)

        # Take top 20 or if is fewer take all available
        top_items = similar_file.head(min(20, len(similar_file)))['item'].tolist()

        # Randomly select 10, if fewer select all recommendations
        if len(top_items) <= num_recommendations:
            return top_items
        return random.sample(top_items, num_recommendations)


    def similar_feature(self, inputs):
        """
        This is a helper method take only one parameter, that Check if input is an artist name,
        track name or track ID, return list of features, if not returns None.
        """
        # Check if input is an artist
        if inputs in self.data:
            return self._artist_features(inputs)

        # Check if input is a track
        for artist, tracks in self.data.items():
            if inputs in tracks:
                return [tracks[inputs].get(f, 0) for f in self.features]
            for track_name, features in tracks.items():
                if features.get('id') == inputs:
                    return [features.get(f, 0) for f in self.features]
        return None

    def _artist_features(self, artist_name):
        """
        This private method take only one parameter, Calculates average features across all
        tracks by an artist. return list of average features, if not return None.
        """
        if artist_name not in self.data:
            return None
        tracks = list(self.data[artist_name].values())
        if not tracks:
            return None
        # Calculate average for each feature across all tracks
        return [Calculate_mean.mean_value([t.get(f, 0) for t in tracks if f in t]) or 0
                for f in self.features]

    def _all_similar(self, input_type):
        """
        This private method take only one parameter, get all items that are similar,
        return all the items with similar type, else return an empty list.
        """
        if input_type == 'artist':
            return list(self.data.keys()) # Return all artist names
        elif input_type == 'track':
            tracks = []
            for artist, artist_tracks in self.data.items():
                tracks.extend(list(artist_tracks.keys())) # Collect all track names
            return tracks
        return []


    def create_dataframe(self):
        """
         This method Creates a pandas DataFrame with artists and their average features,
         return DataFrame with columns 'Artist name' and each feature
        """
        artist_data = []
        for artist in self.data.keys():
            features = self._artist_features(artist)
            if features:  # Only include artists with features
                artist_data.append({'Artist name': artist,
                                    **dict(zip(self.features, features))}) # Combine name and features
        return pd.DataFrame(artist_data)

    def save_dataframe(self, filename='artist_features.csv'):
        """
        This method take only one parameter, Save artist dataframe to CSV file.
        return the dataFrame that was saved.
        """
        df = self.create_dataframe()
        df.head(10).to_csv(filename, index=False)
        return df