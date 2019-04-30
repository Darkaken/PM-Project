def random_solve(vector_list, distance_algorithm, max_count):

    """
    Input:
        a) Vector List (equal length vectors) (type = list)
        b) Distance Algorithm (type = func)
        c) Max Count (type = int)
    Explanation:
        This algorithm shuffles !randomly! the provided list of vectors and uses the …
        algorithm to obtain a local minimum list of vectors and its according total distance. If the new distance
        is better than the previous best, the best distance is redefined as the new distance. If no improvement
        is achieved in {Max Count} cycles, the algorithm stops and returns the best list obtained and the according
        total distance.
    Output:
        a) Best Vector List (type = list)
        b) Best Distance (type = float or int, depending on the distance algorithm)
    """

    best = None
    best_distance = None
    cycle = 0               #Total cycles
    counter = 0

    for number in range(max_count):
    
        
    

    return best, best_distance
