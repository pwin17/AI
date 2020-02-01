                md_list =[]
                for i in transition:
                    md_list.append(abs(ep[0] - i[0]) + abs(ep[1] - i[1]))
                minimum_heuristic = float('inf')
                print(md_list)

                for i in range(len(md_list)):
                    if md_list[i] < minimum_heuristic:
                        minimum_heuristic = md_list[i]
                        position = i
                our_deque.append(transition[position])
                # print(transition[position])
                expanded_nodes+=1