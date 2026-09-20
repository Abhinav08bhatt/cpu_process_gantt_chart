import matplotlib.pyplot as plt

from helper.helper_functions import remove_duplicate

def create_gantt_chart(time_line,question):

    timeline = time_line

    # processes = ["P1","P2","P3","P4"]
    processes = []
    for i in timeline:
        processes.append(i[0])
    print(processes)


    y_position = {}
    position = 0
    for p in processes:
        if p in y_position:
            continue
        y_position[p] = position
        position = position+(len(remove_duplicate(processes)))
    print(y_position)

    fig, (gantt_chart, table_ax) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]})

    points = []
    header_for_table = ["Processes","Arrival T","Burst T","Completion T","Turnaround T","Waiting T"]
    rows_for_table = []

    i = 0
    for process, start, duration in timeline:
        y = y_position[process]

        gantt_chart.broken_barh(
            [(start,duration)],
            (y_position[process], 2),
            facecolors = "lightblue",
            edgecolors = "lightgrey"
        )

        x_center = (start + (start+duration))/2
        y_center = y + 1

        gantt_chart.text(x_center,y_center,process,ha='center',va='center',fontsize=16)
        gantt_chart.text(start+0.1,y_center,start,ha='center',va='center')
        gantt_chart.text((start+duration)-0.1,y_center,start+duration,ha='center',va='center')

        points.append(start)
        points.append(start+duration)

        print("qus : ",question[i])

        #                     ["Processes"   ,"Arrival T"   ,"Burst T"     ,"Completion T"      ,"Turnaround T"                       ,"Waiting T"                                                     ]
        rows_for_table.append([question[i][0],question[i][2],question[i][1],start+question[i][1],(start+question[i][1])-question[i][2],((start+question[i][1])-question[i][2])-question[i][1]])
        i+=1

    gantt_chart.set_xticks(points)

    y_ticks = []
    for y in y_position.values():
        y_ticks.append(y+1)

    print(y_ticks)
    gantt_chart.set_yticks(y_ticks)
    gantt_chart.set_yticklabels(remove_duplicate(processes))

    gantt_chart.set_xlabel("time(millisecond)")
    gantt_chart.set_ylabel("process id")
    gantt_chart.set_title("cpu scheduling gantt chart")

    gantt_chart.set_xlim(0,(timeline[-1][1]+timeline[-1][2]+1))
    gantt_chart.grid(True,color='lightgrey')

    table_ax.axis('off')
    table = table_ax.table(
        cellText=rows_for_table,          # 2D list: [[val1, val2, ...], ...]
        colLabels=header_for_table,      # 1D list: ["Col 1", "Col 2", ...]
        loc='center',           # Anchor: 'top', 'center', 'bottom'
        cellLoc='center'        # Text alignment: 'center', 'left', 'right'
    )

    # TODO : add the IDLE state graph 
        # gantt_chart.axvspan(3, 5, color="lightgrey", alpha=0.15, hatch="//")
        # gantt_chart.text(
        #     4,
        #     y_center,
        #     "IDLE",
        #     ha="center",
        #     va="center",
        #     color="grey",
        #     fontsize=12,
        #     fontstyle="italic",
        # )

    # TODO : add the info about the query : 
    #? [ ] completion time , 
    #? [ ] turnaround time , avg turnaround time
    #? [ ] waiting time , avg waiting time
    #? [ ] cpu utilization , 
    #? [ ] throughput , 

    plt.tight_layout()
    plt.show()



def first_come_first_serve(query,context_switching=0):

    # question = [ [ process_id , cpu-burst , arrival-time ] , [...] ]
    # answer = [ [ process_id , start-time , duration ] , [...] ]

    # TODO : list is a freaking mutable datatype 

    question = query
    question.sort(key=lambda x : x[2])

    answer = []

    waiting = 0

    for i in range (len(question)) :
        if i == 0 :
            waiting = question[0][2]
        elif (answer[i-1][1]+answer[i-1][2]) >= question[i][2]:
            waiting = answer[i-1][1]+answer[i-1][2]
        elif (answer[i-1][1]+answer[i-1][2]) < question[i][2]:
            waiting = question[i][2]

        answer.append([question[i][0],waiting+context_switching,question[i][1]])

    # print(answer)

    return answer




def main():

    # question = [ [ process_id , cpu-burst , arrival-time ] , [...] ]
    # answer = [ [ process_id , start-time , duration ] , [...] ]

    # answer = [
    #     ("P1",0,1),
    #     ("P2",1,3),
    #     ("P3",4,4),
    #     ("P4",9,2),
    #     ("P2",11,3),
    #     ("P3",14,4),
    #     ("P1",18,1),
    # ]

    question = [
        ['P2',5,15],
        ['P1',10,0],
        ['P3',5,15],
        ['P4',10,23],
    ]

    answer = first_come_first_serve(question)

    print(answer)

    create_gantt_chart(answer,question)

main()