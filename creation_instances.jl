include("algorithms.jl")
include("Instances.jl")
using Random 


function create_input_file_scp(
    filename::String, 
    num_students::Int, 
    num_schools::Int, 
    capacities, 
    pref_mode,
    seed,
    incomplete_len
)

    if length(capacities) != num_schools
        error("The length of capacities must match the number of schools.")
    end

    open(filename, "w") do file
        # Write header information
        println(file, "# Num. students:$num_students")
        println(file, "# Num. colleges:$num_schools")

        students = ["s$i" for i in 1:num_students]
        colleges = ["c$j" for j in 1:num_schools]
        println(file, "# Students:" * join(students, ","))
        println(file, "# Colleges:" * join(colleges, ","))

        println(file, "# Capacities:")
        for (i, capacity) in enumerate(capacities)
            println(file, "c$i $capacity")
        end

        rng = MersenneTwister(seed)


        println(file, "# Student preferences:")
        for student in students
            if pref_mode == "Flexible"
                lenght_pref = rand(rng, incomplete_len:num_schools)
            elseif  pref_mode == "Complete"
                lenght_pref = num_schools
            elseif pref_mode == "Incomplete"
                lenght_pref = incomplete_len
            else 
                println("INVALID PREFERRENCES")
            end
            sampled_colleges = shuffle(rng, colleges)[1:lenght_pref]
            pref= join(["($(index),$(element))" for (index, element) in enumerate(sampled_colleges)], " ")
            println(file, "$student " * pref)
        end

        println(file, "# College priorities:")
        for college in colleges
            sampled_students = shuffle(rng, students)
            pref= join(["($(index),$(element))" for (index, element) in enumerate(sampled_students)], " ")
            println(file, "$college " * pref)
        end
    end

    println("File '$filename' created successfully.")
end



function create_match_file(
    filename_input::String,
    filename_match::String
)
    open(filename_match, "w") do file
        SC = read_game_from_txt(filename_input)
        DA_match = DA(SC)
        DA_match_tuple = dict_to_tuples(DA_match)
        println(file, "# DA matching of corresponding input")
        println(file, DA_match_tuple)

    end
    println("File '$filename_match' created successfully.")
end

function create_equal_capacity(totalCap,schools)
    return fill(div(totalCap, schools), schools)
end

function distribute_seats(total_capacity, num_schools,seed)
    if num_schools > total_capacity
        error("Number of schools cannot exceed total capacity.")
    end

    rng = MersenneTwister(seed)

    # Each school gets at least one seat
    seats = ones(Int, num_schools)
    remaining = total_capacity - num_schools

    for _ in 1:remaining
        idx = rand(rng, 1:num_schools)
        seats[idx] += 1
    end

    return seats
end



function dict_to_tuples(d::Dict{String, String})
    tuples = [(k, v) for (k, v) in d]
    return sort(tuples, by = x -> parse(Int, replace(x[1], "s" => "")))
end



# Example usage:
#create_input_file("input_LLM/example_test_2.txt", 6, 4, [2, 1,1,1], 3)
#create_match_file("input_LLM/example_test_2.txt","input_LLM_match/example_test_2.txt")


##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
################################################# CREATION OF THE INSTANCES ##############################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################

number_students = [5]

number_school = Dict(5=> [5,4,3], 10=>[10,5,4,3], 15=> [15,8,5,4],20=>[20,10,7,5],30=> [30,15,10,8])

preferences = ["Incomplete", "Flexible", "Complete"]

Total_capacity = Dict(5=> [4,5,10], 10=> [8,10,15], 15 => [12,15,20],20=> [16,20,25], 30=> [24,30,35])

seeds= [1,2,3]

for n_student in number_students

    for n_school in number_school[n_student]

        for pref_mode in preferences

            for total_cap in Total_capacity[n_student]
                
                for seed in seeds

                    # if nb_school < total_cap : pass
                    if n_school > total_cap 
                        continue
                    else
                        # create the instance
                        school_capacity = distribute_seats(total_cap,n_school,seed)
                        filename_input = "LLM_instances_final/scp_($(n_student),$(n_school))_$(pref_mode)_$(total_cap)_seed$(seed).txt"
                        filename_output = "LLM_match_final/match_scp_($(n_student),$(n_school))_$(pref_mode)_$(total_cap)_seed$(seed).txt"

                        create_input_file_scp(filename_input,n_student,n_school,school_capacity,pref_mode,seed,1)
                        create_match_file(filename_input,filename_output)
                    end

                end
            end


        end


    end

end
