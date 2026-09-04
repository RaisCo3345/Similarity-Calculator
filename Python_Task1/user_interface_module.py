import tkinter
from similarity_module import SimilarityCalculator

class musicSimilarityGUI:
    """
    This class allow user to compare similarities between two Musics,
    you can only compare by track name, artist name or id, if not it
    display an error message, find top 5 similar artist using similarity metrix
    """
    def __init__(self, data_file):
        """
        The constructor, declare all the class variables, set up our window and
        configure it is properties, organize all the GUI components and prepare
        similarity checks with provided data.
        """
        self.data_file = data_file
        self.calculate_similarity = SimilarityCalculator(data_file)
        self.window = tkinter.Tk()
        self.window.configure(background="#42EAFF")
        self.window.title("SIMILARITY CALCULATOR")
        self.window.geometry("600x800")
        self.window.grid_columnconfigure(0, weight=1) #Make column 0 expand horizontally when window resize
        self.window.grid_rowconfigure(4, weight=1)  #Make row 4 (results area) expand vertically


        # Create title label at the top center
        tkinter.Label(self.window, text="MUSIC SIMILARITY",font=("Times New Roman", 20, "bold"),
                      bg="#42EAFF").grid(row=0, column=0, pady=15)

        # This Section Create Compare Items Frame
        compare_items_frame = tkinter.LabelFrame(self.window, text="COMPARE ITEMS",
                                                 font=("DejaVuSans", 12, "bold"),padx=20, pady=10, bg="#42EAFF")
        compare_items_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        compare_items_frame.grid_columnconfigure(1, weight=1)

        #This Creates input field and text input for item 1
        tkinter.Label(compare_items_frame, text="Item 1:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=0, column=0, sticky="w", pady=5)
        self.input1 = tkinter.Entry(compare_items_frame, width=35, font="DejaVuSans 10")
        self.input1.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        #This Creates input field and text entry for item 2
        tkinter.Label(compare_items_frame, text="Item 2:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=1, column=0, sticky="w", pady=5)
        self.input2 = tkinter.Entry(compare_items_frame, width=35, font="DejaVuSans 10")
        self.input2.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        #This Creates a radio button section for the type of item(Artist, Track and Id)
        tkinter.Label(compare_items_frame, text="Type:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=2, column=0, sticky="w", pady=5)
        type_frame = tkinter.Frame(compare_items_frame, bg="#42EAFF")
        type_frame.grid(row=2, column=1, pady=5, sticky="w")
        self.type_var = tkinter.StringVar(value="artist")
        for button, (text, item) in enumerate([("Artist", "artist"), ("Track", "track"), ("ID", "id")]):
            tkinter.Radiobutton(type_frame, text=text, variable=self.type_var,value=item,
                                font=("DejaVu Sans", 9), bg="#42EAFF").grid(row=0, column=button, padx=5)

        #This Creates a radio button section for the metrics (Pearson, Cosine, Euclidean and Manhattan)
        tkinter.Label(compare_items_frame, text="Metric:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=3, column=0, sticky="w", pady=5)
        metric_frame = tkinter.Frame(compare_items_frame, bg="#42EAFF")
        metric_frame.grid(row=3, column=1, pady=5, sticky="w")
        # euclidean as Default
        self.metric_var = tkinter.StringVar(value="euclidean")
        for button, (text, item) in enumerate([("Euclidean", "euclidean"), ("Cosine", "cosine"),
                                           ("Pearson", "pearson"), ("Manhattan", "manhattan")]):
            tkinter.Radiobutton(metric_frame, text=text, variable=self.metric_var,value=item,
                                font=("DejaVu Sans", 9), bg="#42EAFF").grid(row=0, column=button, padx=3)


        # This Create Find Top 5 Similar Artists Frame
        find_top5_frame = tkinter.LabelFrame(self.window, text="FIND TOP 5 SIMILAR ARTIST",
                                        font=("DejaVu Sans", 12, "bold"),padx=10, pady=10, bg="#42EAFF")
        find_top5_frame.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
        find_top5_frame.grid_columnconfigure(1, weight=1)

        # This Creates input field and text entry for Artist name
        tkinter.Label(find_top5_frame, text="Artist Name:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=0, column=0, sticky="w", pady=5)
        self.top5_input = tkinter.Entry(find_top5_frame, width=30, font="DejaVuSans 10")
        self.top5_input.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        # This Creates radio button for top5 metrics (Euclidean, Cosine and Pearson)
        tkinter.Label(find_top5_frame, text="Metric:", font=("DejaVuSans", 10, "bold"),
                      bg="#42EAFF").grid(row=1, column=0, sticky="w", pady=5)
        top5_metric_frame = tkinter.Frame(find_top5_frame, bg="#42EAFF")
        top5_metric_frame.grid(row=1, column=1, pady=5, sticky="w")
        # Euclidean as Default
        self.top5_metric_var = tkinter.StringVar(value="euclidean")
        for button, (text, item) in enumerate([("Euclidean", "euclidean"), ("Cosine", "cosine"),
                                           ("Pearson", "pearson")]):
            tkinter.Radiobutton(top5_metric_frame, text=text, variable=self.top5_metric_var,value=item,
                                font="DejaVuSans 10", bg="#42EAFF").grid(row=0, column=button, padx=3)


        # This Section Creates Button, start by creating button frame
        button_frame = tkinter.Frame(self.window, bg="#42EAFF")
        button_frame.grid(row=3, column=0, pady=15)
        # Score button with appropriate width and background(green), font(white) color
        tkinter.Button(button_frame, text="Score", command=self.score, width=15,
                      bg="green", fg="white", font=("DejaVuSans", 10, "bold")).grid(row=0, column=0, padx=5)
        # Find Top 5 button with appropriate width and background(blue), font(white) color
        tkinter.Button(button_frame, text="Find Top 5", command=self.find_top5, width=15,
                      bg="blue", fg="white", font=("DejaVuSans", 10, "bold")).grid(row=0, column=1, padx=5)
        # Clear button with appropriate width and background(gray), font(white) color
        tkinter.Button(button_frame, text="Clear", command=self.clear, width=15,
                      bg="gray", fg="white", font=("DejaVuSans", 10, "bold")).grid(row=0, column=2, padx=5)
        # Quit button with appropriate width and background(red), font(white) color
        tkinter.Button(button_frame, text="Quit", command=self.window.quit, width=15,
                      bg="red", fg="white", font=("DejaVuSans", 10, "bold")).grid(row=0, column=3, padx=5)


        # This Creates Result Display Section, start by creating frame
        result_frame = tkinter.LabelFrame(self.window, text="RESULTS",font=("DejaVuSans", 12, "bold"),
                                         padx=10, pady=10, bg="#42EAFF")
        result_frame.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        self.result_text = tkinter.Text(result_frame, height=20, width=75, font="DejaVuSans 10", bg="white", padx=10, pady=10)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        # This creates a right scroll bar
        scrollbar = tkinter.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)

    def score(self):
        """
        This method is called when the user click the score button,
        it calculated the similarity score between input1 and input2,
        first it check for input validation and input type are correct.
        """
        input1, input2 = self.input1.get().strip(), self.input2.get().strip()
        input_type, metric_type = self.type_var.get(), self.metric_var.get()
        # Check that the user enter test input, if not display message.
        if not input1 or not input2:
            return self.error_display("Please enter both items to compare.")

        try:
            # call input validation in similarity module to validate the user input.
            similarity = self.calculate_similarity.input_validation(
                input1, input_type,
                input2, input_type,
                metric_type
            )
            # This dictionary define a value for different similarity level, and value <= 0.3 is very low
            result_interpretations = {0.9: "Very High", 0.7: "High", 0.5: "Moderate", 0.3: "Low"}
            interpret = next((value for key, value in result_interpretations.items() if similarity > key), "Very Low")
            # This display the results in side the frame, top and bottom borderline, title, inputs etc.
            result = f"{'='*60}\n"
            result += f"  SIMILARITY COMPARISON RESULT\n"
            result += f"{'='*60}\n\n"
            result += f"  Input 1:     {input1}\n"
            result += f"  Type:       {input_type.capitalize()}\n"
            result += f"  Input 2:     {input2}\n"
            result += f"  Type:       {input_type.capitalize()}\n"
            result += f"  Metric:     {metric_type.capitalize()}\n\n"
            result += f"  {'─'*50}\n"
            result += f"  Similarity Score:  {similarity:.4f}\n"
            result += f"  Interpretation:    {interpret} Similarity\n"
            result += f"{'='*60}\n"
            self.result_display(result) # call display the result
        # if input validation fails, it catsh valur error or any other error.
        except ValueError as e:
            self.error_display(f"Validation Error: {str(e)}")
        except Exception as e:
            self.error_display(f"Error: {str(e)}")

    def find_top5(self):
        """
        This method uses the given artist name and metric to fine the top 5 similar
        with the same similarities, if artist not found it display error message
        """
        artist_name = self.top5_input.get().strip()
        metric = self.top5_metric_var.get()
        # check if artist is in the data
        if not artist_name:
            self.error_display("Please enter an artist name.")
            return

        try:
            # This uses the validation method
            top5 = self.calculate_similarity.top5_artists_validation(artist_name, metric)
            # if the artist not found it display message
            if not top5:
                self.error_display(f"No similar artists found for '{artist_name}' with similarity > 0.8 using {metric} metric.")
            # display the top5 result, create top and bottom borderlines, title, artist name and metric.
            else:
                result = f"{'='*60}\n"
                result += f"  TOP 5 SIMILAR ARTISTS\n"
                result += f"{'='*60}\n\n"
                result += f"  Artist:     {artist_name}\n"
                result += f"  Metric:     {metric.capitalize()}\n\n"
                result += f"  {'─'*50}\n"
                result += f"  Similar Artists:\n\n"
                for i, artist in enumerate(top5, 1):
                    result += f"  {i}. {artist}\n"
                result += f"{'='*60}\n"
                self.result_display(result)
        # if top5 validation fails, it catsh value error or any other error.
        except ValueError as e:
            self.error_display(f"Validation Error: {str(e)}")
        except Exception as e:
            self.error_display(f"Error: {str(e)}")

    def result_display(self, text):
        """
        This is a helper method that clear existing text from index 1 in the result display
        and invert the new text to display from index 1.
        """
        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(1.0, text)

    def error_display(self, message):
        """
        This is a helper method that clear the existing text from index 1
        and display the error message from index i.
        """
        self.result_text.delete(1.0, tkinter.END)
        error_message = f"{'='*60}\n"
        error_message += f"  ERROR\n"
        error_message += f"{'='*60}\n\n"
        error_message += f"  {message}\n"
        error_message += f"{'='*60}\n"
        self.result_text.insert(1.0, error_message)

    def clear(self):
        """
        # This method is called when you click the clear button, it clears all text in the result text,
        the two inputs and top5 input, set them to the initial and reset all radio button to default.
        """
        self.input1.delete(0, tkinter.END)
        self.input2.delete(0, tkinter.END)
        self.top5_input.delete(0, tkinter.END)
        self.result_text.delete(1.0, tkinter.END)
        self.type_var.set("artist")
        self.metric_var.set("euclidean")
        self.top5_metric_var.set("euclidean")

    def run(self):
        """
        This method start the tkinter that handle all the GUI.
        application will run until the user click Quit button.
        """
        self.window.mainloop()