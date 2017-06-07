#encoding=utf-8
import json
import numpy
import operator
'''
list =[[110.6,174.6 ,560.7, 205.7], [306.3, 274.5, 532.6, 303.6], [323.4 ,225.8, 551.6, 255.6],
       [467.0, 370.1, 600.2, 398.0],  [256.4, 372.8 ,390.1, 400.5], [109.3 ,128.0, 190.3 ,157.5],
       [107.8, 79.4, 216.3, 108.5],  [289.6, 324.3, 387.0 ,352.1], [374.5, 79.8, 479.1, 109.2],
       [112.6, 225.7, 194.2, 255.0]]

list2 =[[ 121.8 ,160.2, 541.5, 193.3], [119.4, 206.0,  309.6,  235.3], [295.0,  299.4 , 523.9 , 328.9],
       [472.4,  358.4,  602.3,  387.1], [262.6,  358.6 , 391.7 , 386.9],[126.5 , 68.5,  233.5 , 97.5],
       [125.0,  114.4,  203.6 , 143.2], [279.5 , 254.2,  375.9,  281.6], [491.1 , 210.4,  571.1,  239.4],
       [424.5,  73.0,  476.4,  101.7]]

list3 =[[ 323.5, 237.5,  535.2,  267.6], [303.7 , 285.6 , 531.0,  315.6], [252.3,  381.2,  386.2,  409.2],
       [287.8,  333.8 , 423.7 , 362.0], [108.8, 167.4, 568.2,  198.6], [462.2,  383.1,  596.9,  410.9],
       [109.5,  88.5,  218.3,  117.6], [375.2,  91.4,  533.5,  122.0], [111.2,  234.9,  190.9,  264.0],
       [ 110.7,  137.8,  188.9,  165.7], [114.6,  194.5,  181.1,  221.1]]
list4 = [[295.6, 297.3, 519.0,326.6], [115.5, 207.4, 356.6, 237.8], [275.4, 252.5, 396.6, 280.6],
        [112.1, 71.6, 219.9, 99.9], [471.3, 348.7, 597.6, 376.2], [414.4, 72.5, 517.5, 100.7],
        [487.1, 203.9, 565.0, 232.5], [113.7, 119.0, 191.9, 145.8],[125.9, 148.2, 596.3, 177.5],
        [273.3, 355.6, 391.3, 381.6],[112.0, 172.4, 308.6, 203.3]]
'''
list = [[336.4, 239.3, 527.7, 269.0], [315.3, 287.3, 546.4, 318.7],[260.7, 385.8, 396.6, 413.7],
        [122.6, 185.2, 619.9, 219.7], [472.4, 387.1, 605.5, 413.9],[294.9, 337.3, 445.0, 366.7],
        [124.5, 86.8, 229.6, 115.5], [120.8, 136.7, 202.6, 165.6], [392.2, 91.8, 498.6, 121.2],
        [121.2, 233.6, 202.2, 262.6], [395.0, 149.4, 453.2, 174.7]]
confid = [1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.999, 0.999, 0.999, 0.054]


# input regions is [[left,top, right, bottom, confidence_score]]
def align(regions, conf_thred = 0.81):
    conf_regions = [ region for region in regions if region[4] > conf_thred]

    # sort the region by Y
    sorted_regions = sorted(conf_regions, key=lambda x: x[1])
    region_count = len(sorted_regions)
    if region_count == 10 or region_count == 11:
        # palte no/vechile type, model/use charactor, register date/issue date, are in the same line
        # need to check their postion by X
        adjust_field_index = [0, 5, 9] if region_count == 11 else [0, 4, 8]
        for index in adjust_field_index:
            # sort by X
            if sorted_regions[index][0] > sorted_regions[index + 1][0]:
                sorted_regions[index], sorted_regions[index + 1] = sorted_regions[index + 1], sorted_regions[index]

        # check the license version, and adjust the layout for the old version license
        vin_index, engine_index = [7, 8] if region_count == 11 else [6, 7]
        propetry_width = sorted_regions[5][2] - sorted_regions[5][0] if region_count == 11 else sorted_regions[4][2] - sorted_regions[4][0]
        if propetry_width > 85.0:
            # old version, adjust model/use charactor  and vin/engion no
            sorted_regions[vin_index], sorted_regions[engine_index] = sorted_regions[engine_index], sorted_regions[
                vin_index]
            use_index = adjust_field_index[1]
            model_index = use_index + 1
            sorted_regions[use_index], sorted_regions[model_index] = sorted_regions[model_index], sorted_regions[
                use_index]

    return sorted_regions

if __name__ == '__main__':
    for i in range(len(list)):
        list[i].append(confid[i])
    
    print(align(list))
    print "Finish！"
