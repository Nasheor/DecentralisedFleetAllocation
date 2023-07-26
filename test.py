def run_vectorization_analysis(self, keywords):
    """
    Run keyword analysis using the TF-IDF vectorization approach.

    Args:
        keywords: List of KeyWordDetails objects.

    Returns:
        List of lists of similar keyword objects.
        The reference keyword is added to the matched_keywords list.
        If the inner list only contains one item, it means no other matches were found.
        If matches were found, the inner list will contain multiple keyword objects.
    """
    groups = []  # This will hold the lists of matched keyword objects
    matched_keywords = []  # Matched keyword objects are collected here.

    # Convert keywords into a list of strings
    keyword_strings = [kw.keyword for kw in keywords]

    # Create a TF-IDF vectorizer to convert keywords into numerical vectors
    vectorizer = TfidfVectorizer()
    keyword_vectors = vectorizer.fit_transform(keyword_strings)

    while len(keywords) > 0:  # Keep looping until all elements are analyzed
        # Get the first keyword
        reference_keyword = keywords.pop(0)
        # Add the reference keyword to the matched list
        matched_keywords.append(reference_keyword)
        match_indices = []  # Clear the matches found

        for i in range(len(keywords)):
            target_keyword = keywords[i].keyword
            # Convert the target keyword to a vector
            target_vector = vectorizer.transform([target_keyword])
            # Calculate the cosine similarity between the reference and target vectors
            similarity_score = linear_kernel(keyword_vectors[0], target_vector)[0][0]

            if similarity_score >= 0.5:  # Set a threshold for similarity (adjust as needed)
                match_indices.append(i)

        # Work through all of the matches found and remove them from the list of keywords to be scanned.
        # Remove the elements in reverse order
        for i in reversed(match_indices):
            matched_keywords.append(keywords.pop(i))

        # Put this list of matched keywords into the groups list
        groups.append(matched_keywords)
        # Clear the matched keywords for the next iteration
        matched_keywords = []

    self.matching_results = groups