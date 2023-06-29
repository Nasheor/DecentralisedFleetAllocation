# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------


# ------------------------------------------
# IMPORTS
# ------------------------------------------
import docplex.mp.model


# ----------------------------------------------------------
# FUNCTION 01 - solve_compute_optimal_EV_2_SEC_allocation
# ----------------------------------------------------------
def solve_compute_optimal_EV_2_SEC_allocation(ub_TPs,
                                              num_SECs,
                                              num_EVs,
                                              array_values,
                                              time_limit
                                             ):

    # -----------------------
    # 1. OUTPUT VARIABLES
    # -----------------------

    # 1. We create the output variables
    res = ()

    # 1.1. We output the search status
    succeed = -1

    # 1.2. We output the amount of TPs satisfied
    best_value = -1

    # 1.3. We output the amount of vehicles per SEC
    EV_per_SEC = [0] * num_SECs


    # -----------------------
    # 2. MODEL CREATION
    # -----------------------

    # 1. We create the model
    mdl = docplex.mp.model.Model(name='EV_2_SEC_allocation')

    # -----------------------
    # 3. DECISION VARIABLES
    # -----------------------

    # 1. We create a list of boolean variables, specifying if each SEC_i picks or not an specific number of vehicles j
    my_vars = mdl.binary_var_list(num_SECs * (num_EVs + 1), name="my_vars")

    # 2. We create an integer variable, specifying the total number of trips satisfied
    my_opt_var = mdl.integer_var(lb=0, ub=ub_TPs, name="my_opt_var")

    # -----------------------
    # 4. CONSTRAINTS
    # -----------------------

    # 1. We add the constraint ensuring all EVs are allocated to the SECs
    amount_of_EVs = [ index % (num_EVs + 1)  for index in range(num_SECs * (num_EVs + 1)) ]
    mdl.add_constraint(mdl.sum(my_vars[i] * amount_of_EVs[i] for i in range(num_SECs * (num_EVs + 1))) == num_EVs)

    # 2. We add the constraint ensuring each SEC is allocated a given amount of EVs
    for SEC_index in range(num_SECs):
        mdl.add_constraint(mdl.sum(my_vars[i] for i in range(SEC_index * (num_EVs + 1), (SEC_index + 1) * (num_EVs + 1))) == 1)

    # 3. We add the constraint for defining the optimisation function
    mdl.add_constraint(my_opt_var == mdl.sum(my_vars[i] * array_values[i] for i in range(num_SECs * (num_EVs + 1))))


    # ----------------------------
    # 5. OPTIMISATION FUNCTION
    # ----------------------------

    # 1. We maximise the cost of my_opt_var
    mdl.maximize(my_opt_var)

    # ----------------------------
    # 6. SOLVE
    # ----------------------------

    # 1. We try to solve the problem
    mdl.set_time_limit(time_limit)
    if (mdl.solve()):
        # 1.1. We update succeed
        succeed = 0
        if (mdl.solve_details.gap == 0.0):
            succeed = 1

        # 2.2. We update best_value
        best_value = int(my_opt_var.solution_value)

        # 2.3. We update EV_per_SEC
        for SEC_index in range(num_SECs):
            value = 0
            for index in range(SEC_index * (num_EVs + 1), (SEC_index + 1) * (num_EVs + 1)):
                if (my_vars[index].solution_value < 0.1):
                    value += 1
                else:
                    break
            EV_per_SEC[SEC_index] = value

    # ----------------------------
    # 8. ASSIGN OUTPUT VARIABLES
    # ----------------------------

    # 1. We assign res
    res = (succeed,
           best_value,
           EV_per_SEC
          )

    # 2. We return res
    return res


# ----------------------------------------------------------------
# FUNCTION 02 - solve_compute_optimal_SEC_negotiation_schedule
# ----------------------------------------------------------------
def solve_compute_optimal_SEC_negotiation_schedule(num_nodes,
                                                   edges_per_node,
                                                   best_value,
                                                   time_limit
                                                   ):
    # -----------------------
    # 1. OUTPUT VARIABLES
    # -----------------------

    # 1. We create the output variables
    res = ()

    # 1.1. We output the search status
    succeed = -1

    # 1.2. We get the new_colours
    colour_per_node = [-1] * num_nodes

    # -----------------------
    # 2. MODEL CREATION
    # -----------------------

    # 1. We create the model
    mdl = docplex.mp.model.Model(name='graph_colouring')

    # -----------------------
    # 3. DECISION VARIABLES
    # -----------------------

    # 1. We create a list of integer variables, specifying the colour selected for each item
    my_vars = mdl.integer_var_list(num_nodes, lb=0, ub=best_value - 2, name="my_vars")

    # 2. We create an integer variable, specifying the total number of colours used
    my_opt_var = mdl.integer_var(lb=1, ub=best_value - 1, name="my_opt_var")

    # -----------------------
    # 4. CONSTRAINTS
    # -----------------------

    # 1. We traverse the nodes to add the frontier constraints
    for node_id in range(num_nodes):
        # 1.1. Given a node "node_id" we get its list of neighbours
        neighbours = edges_per_node[node_id][1]

        # 1.2. For each neighbour we impose a non-equal constraint
        for new_node in neighbours:
            mdl.add_constraint(my_vars[node_id] != my_vars[new_node])

    # 2. We add the symmetry breaking constraints
    add_symmetry = False

    # 2.1. We traverse all nodes
    for node_id in range(num_nodes):
        # 2.1.1. We get the number of neighbours
        info = edges_per_node[node_id]

        # 2.1.2. If the node has at least one neighbour and the symmetry constraint was not added
        if ((info[0] > 0) and (add_symmetry == False)):
            # I. We add the constraint to colour with 0 the node
            mdl.add_constraint(my_vars[node_id] == 0)

            # II. We add the constraint to colour with 1 its first neighbour
            first_neighbour_node = info[1][0]
            mdl.add_constraint(my_vars[first_neighbour_node] == 1)

            # III. We mark the symmetry constraint as already added
            add_symmetry = True

        # 2.1.3. If the node has zero neighbours we colour it as zero
        elif (info[0] == 0):
            mdl.add_constraint(my_vars[node_id] == 0)

    # 3. We add the constraints around the optimisation variable
    for node_id in range(num_nodes):
        mdl.add_constraint(my_opt_var >= my_vars[node_id] + 1)

    # ----------------------------
    # 5. OPTIMISATION FUNCTION
    # ----------------------------

    # 1. We minimise the cost of my_opt_var
    mdl.minimize(my_opt_var)

    # ----------------------------
    # 6. SOLVE
    # ----------------------------

    # 1. We try to solve the problem
    mdl.set_time_limit(time_limit)
    if (mdl.solve()):
        # 1.1. We update succeed
        succeed = 0
        if (mdl.solve_details.gap == 0.0):
            succeed = 1

        # 2.2. We update best_value
        best_value = my_opt_var.solution_value

        # 2.3. We update new_colours
        for index in range(num_nodes):
            colour_per_node[index] = int(my_vars[index].solution_value)

    # ----------------------------
    # 8. ASSIGN OUTPUT VARIABLES
    # ----------------------------

    # 1. We assign res
    res = (succeed,
           best_value,
           colour_per_node
           )

    # 2. We return res
    return res

