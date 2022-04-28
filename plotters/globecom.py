import csv
import math
from scipy.stats import genpareto
import matplotlib.pyplot as plt
import numpy as numpy
import random
import numpy as np
import statistics
import csv
import matplotlib
from matplotlib.ticker import MaxNLocator
from torus_integrated.myglobal import *

waa_load_total_bps_avg_INTRA_2400=[0, 0, 64336320000.0, 0, 0, 0, 205465280000.0, 0, 259183520000.0, 297512768000.0, 332882752000.0, 360567532307.6923, 399899388235.2941, 433001803636.36365, 469549653333.3333, 501215520000.0, 534287314285.7143, 558586048000.0, 598248480000.0, 633204720000.0, 658416240000.0, 699602240000.0, 735977600000.0, 763060373333.3334, 1703434560000.0]
waa_thru_total_bps_avg_INTRA_2400=[0, 0, 348339200000.0, 0, 0, 0, 344575040000.0, 0, 351936160000.0, 355473216000.0, 354329728000.0, 353539815384.61536, 354568395294.1177, 353487825454.5455, 354938880000.0, 354905813333.3333, 355448091428.5714, 355676416000.0, 355511466666.6667, 356267680000.0, 355644720000.0, 355380160000.0, 356808160000.0, 357324053333.3333, 356950080000.0]
waa_drop_total_bps_avg_INTRA_2400=[0, 0, 0.0, 0, 0, 0, 0.0, 0, 3256800000.0, 20345600000.0, 34161472000.0, 39467224615.38461, 69243821176.47058, 95150516363.63637, 93375200000.0, 156446720000.0, 135668982857.14285, 179431552000.0, 230231893333.33334, 259670320000.0, 207920800000.0, 161368640000.0, 331131840000.0, 346214720000.0, 391743360000.0]
waa_delay_total_avg_INTRA_2400=[0, 0, 8.190776595298717e-06, 0, 0, 0, 8.52985848907896e-06, 0, 2.7231091565164905e-05, 4.972119191185181e-05, 8.356664890512059e-05, 7.057304978980352e-05, 6.399436254081459e-05, 6.885605540417052e-05, 8.984991260895859e-05, 9.275613688270343e-05, 0.00010044435744403432, 0.00010753362243158872, 0.00010314483430357878, 0.00013348844451705955, 0.0001003926246294903, 0.00018397087380033947, 0.0001754769769687021, 0.00017268169634034676, 0.00021051634930423942]
waa_delay_high_avg_INTRA_2400=[0, 0, 0, 0, 0, 0, 3.713267051097985e-07, 0, 4.3594101043527433e-07, 4.809864635452807e-07, 4.765595885466927e-07, 4.512392823085685e-07, 4.789145556687555e-07, 4.6161658813789224e-07, 4.836042415674303e-07, 4.832619409164648e-07, 4.929560006633238e-07, 5.421247548702698e-07, 4.980505023178619e-07, 5.175943467027281e-07, 5.070489191569777e-07, 4.818359172295345e-07, 5.518620549611916e-07, 5.448423825916283e-07, 5.810484326911706e-07]
waa_delay_med_avg_INTRA_2400=[0, 0, 1.0744463724910999e-05, 0, 0, 0, 7.202297618766787e-05, 0, 0.00015949845211773715, 0.000251324827221763, 0.00044663138977305537, 0.0003101456010411386, 0.00024924368223752614, 0.0002724317640847317, 0.0002921397401872367, 0.00033410163454688596, 0.00035464857287572797, 0.00041270561882466623, 0.0003328194156907169, 0.0004026728391647896, 0.00021112293567915102, 0.0005205732600483074, 0.0005977997370089064, 0.0005666449440478023, 0.00014049328837007825]
waa_delay_low_avg_INTRA_2400=[0, 0, 5.161984883432988e-06, 0, 0, 0, 2.521816444284487e-05, 0, 3.626985769575503e-05, 0.00015328350610405877, 0.0001514084913134023, 0.00021372426147048257, 0.0002833959597602862, 0.00028362548039949527, 0.000344969913029732, 0.00040227393719378664, 0.0003067312235737672, 0.0003770646842549973, 0.00042943287902326617, 0.0005768606702791408, 0.0004370815998581273, 0.00046621342482162947, 0.0005842445808901817, 0.0005195374363934918, 0.00042360191812356265]

waa_load_total_bps_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 815265120000.0, 845290144761.9048, 870094560000.0, 964985760000.0]
waa_thru_total_bps_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 815197088000.0, 845295142857.1428, 869442240000.0, 962245920000.0]
waa_drop_total_bps_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]
waa_delay_total_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.4069880662788047e-07, 3.4467290507380233e-07, 3.612340969130636e-07, 3.770781638382821e-07]
waa_delay_high_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
waa_delay_med_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.315680574265739e-07, 3.325099021003456e-07, 3.386661671483468e-07, 3.6191156668790066e-07]
waa_delay_low_avg_INTER_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.6605693737515136e-07, 3.686918574390985e-07, 3.8361301073026606e-07, 4.0365459285978955e-07]

waa_load_total_bps_avg_E2E_2400=[0.0, 0, 0, 0, 0, 0, 0, 0, 4528840320000.0, 5029065428571.429, 5504396591304.348, 6044742988034.1875, 6603975307216.494, 7124963062857.142, 7673097552941.176, 8238321347368.42, 8749175999999.999, 9261313280000.0, 9821645333333.334, 10201436800000.0, 10980452800000.0, 11532692800000.0, 12010214399999.998, 0, 20224307200000.0]
waa_thru_total_bps_avg_E2E_2400=[4443995200000.0, 0, 0, 0, 0, 0, 0, 0, 4809240960000.0, 4780945542857.143, 4793549530434.782, 4799146789743.59, 4815216890721.649, 4830948411428.571, 4838449788235.294, 4852305852631.579, 4861937066666.667, 4867875200000.0, 4864826400000.0, 4854908000000.0, 4854117600000.0, 4864590400000.0, 4874764800000.0, 0, 4848767040000.0]
waa_drop_total_bps_avg_E2E_2400=[0.0, 0, 0, 0, 0, 0, 0, 0, 458864640000.0, 771552914285.7142, 1058308591304.3478, 1432583398290.5981, 1827704527835.0515, 2309981394285.7144, 2668315529411.7646, 3122427452631.5786, 3338328533333.333, 3665464639999.9995, 3826409600000.0, 3868431200000.0, 3754762399999.9995, 3632755199999.9995, 3572738399999.9995, 0, 2786740800000.0]
waa_delay_total_avg_E2E_2400=[0, 0, 0, 0, 0, 0, 0, 0, 4.603804489034985e-05, 4.973047252216054e-05, 6.104526469636508e-05, 7.423144100772505e-05, 8.94892877167887e-05, 0.00011105094379804054, 0.00012127062517047044, 0.00014594911641564737, 0.00015065520584439638, 0.00016220024063289657, 0.00016167867113663867, 0.00017689506340721724, 0.00016028787523847063, 0.00013660656420712468, 0.00016185135558849232, 0, 0.00018515307282399813]
waa_delay_high_avg_E2E_2400=[0, 0, 0, 0, 0, 0, 0, 0, 4.511505206810167e-07, 4.4840654614526196e-07, 4.554584506225358e-07, 4.642676804984397e-07, 4.818498216370652e-07, 4.900813658103036e-07, 5.054770679556213e-07, 5.362855352278364e-07, 5.26370769725252e-07, 5.674180639570514e-07, 5.744769226573749e-07, 5.511708270645577e-07, 5.852737354488543e-07, 5.7803886028392e-07, 5.933578429995723e-07, 0, 5.874376477536382e-07]
waa_delay_med_avg_E2E_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0.00022708390066910927, 0.00023365347671921283, 0.0002756304649500633, 0.0003291255165398825, 0.00039198646809584717, 0.0004977169882321727, 0.0005311293900980506, 0.0006100677789454736, 0.0006407606029967505, 0.0005986116451576538, 0.0005453441869085937, 0.0007118801752702361, 0.00039461548474275035, 0.0002323272999619965, 0.00029589316232695806, 0, 0.0001677088248982167]
waa_delay_low_avg_E2E_2400=[0, 0, 0, 0, 0, 0, 0, 0, 0.00035105476871217573, 0.0003181230092912008, 0.00035860418556380466, 0.0003775818995350397, 0.00041140597366543094, 0.00047267258638045097, 0.0004911879497571113, 0.000572714894908511, 0.0005270080359663103, 0.0006472540238409928, 0.0006386494860369407, 0.0004959727650731306, 0.0006029735176196586, 0.0005939152662321145, 0.0005978751693947283, 0, 0.0005182458069922384]

waa_load_total_bps_avg_INTRA_3200=[0, 27412480000.0, 0, 0, 0, 0, 317018240000.0, 346851626666.6667, 401308754285.7143, 453519565714.2857, 500080106666.6667, 551970647272.7273, 598292202666.6666, 646866960000.0, 703042826666.6666, 741212960000.0, 812076000000.0, 857243840000.0, 904430080000.0, 950732160000.0, 0, 1040699840000.0, 1079265600000.0, 1140582400000.0, 2093692160000.0]
waa_thru_total_bps_avg_INTRA_3200=[0, 30679360000.0, 0, 0, 0, 0, 426488640000.0, 425762773333.3333, 464095680000.0, 477420182857.1429, 515631808000.0, 524097861818.1818, 519800896000.0, 521742280000.0, 533835680000.0, 537090160000.0, 539543040000.0, 537940480000.0, 539517440000.0, 538215040000.0, 0, 538774720000.0, 541913920000.0, 539608400000.0, 539829120000.0]
waa_drop_total_bps_avg_INTRA_3200=[0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 625920000.0, 13574217142.857143, 33741845333.333332, 39463796363.63636, 74668565333.33333, 118839080000.0, 194880426666.66666, 225640640000.0, 288515680000.0, 317021280000.0, 283593920000.0, 173394880000.0, 0, 411760640000.0, 435776960000.0, 419476080000.0, 620935680000.0]
waa_delay_total_avg_INTRA_3200=[0, 3.4843330419718294e-07, 0, 0, 0, 0, 5.594417496117596e-06, 1.910757885924131e-06, 5.471166220172689e-06, 1.2893629797073742e-05, 2.1708190350789858e-05, 2.4292522577007875e-05, 2.8794611770801504e-05, 2.9099407028797562e-05, 5.6001223326284835e-05, 7.470909074124777e-05, 6.899617375229413e-05, 9.166388214725002e-05, 8.631041809319026e-05, 5.10195993699597e-05, 0, 0.00012224858413775375, 0.0001236164123875677, 0.0001003673373458883, 0.00013291381130621312]
waa_delay_high_avg_INTRA_3200=[0, 0, 0, 0, 0, 0, 2.937340355078634e-07, 2.98002641342245e-07, 3.190164887152044e-07, 3.303541142191452e-07, 3.6432420659578887e-07, 3.747566736093026e-07, 3.7737538191355816e-07, 3.705318858106194e-07, 4.06049309981982e-07, 4.246361005339974e-07, 4.3871722439819404e-07, 4.3385323693780404e-07, 4.4270929281278544e-07, 4.090411458877667e-07, 0, 4.292070183940878e-07, 4.5974448371860303e-07, 4.472394604791977e-07, 4.6827968288369573e-07]
waa_delay_med_avg_INTRA_3200=[0, 4.191570526056469e-07, 0, 0, 0, 0, 3.503865293908362e-05, 5.626283089362227e-06, 2.1014960047343546e-05, 4.910729263240079e-05, 7.22426874517222e-05, 6.553927613895461e-05, 8.392391607806623e-05, 7.406180558642028e-05, 0.00018174350323309514, 0.00025396912040841435, 0.00020903335020812367, 0.00027860187555335845, 0.00021262489821791716, 6.672739933828588e-05, 0, 0.0003468288485565321, 0.0002996952619567829, 0.00023006022118497458, 7.447065021720339e-05]
waa_delay_low_avg_INTRA_3200=[0, 3.213960563146716e-07, 0, 0, 0, 0, 3.7316227976529347e-07, 2.0797156599080587e-05, 3.007962236495464e-05, 5.817203616762286e-05, 8.79734488317237e-05, 0.0001200687558523717, 0.00013177957660501075, 0.0001549920651586886, 0.00022394188896254346, 0.00026880438247246216, 0.0002872422490863934, 0.00031370315926906975, 0.0003037120169601741, 0.0001931158641412544, 0, 0.00035606530108488866, 0.00043775445438110506, 0.0002959446483270727, 0.0003017812121577734]

waa_load_total_bps_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 449299200000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1141061963636.3635, 1195317211428.5715, 1244477207272.7273, 1304510720000.0, 1350745218461.5386]
waa_thru_total_bps_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 455869120000.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1141225047272.7273, 1195523306666.6667, 1244606661818.182, 1304230787368.4211, 1349665858461.5386]
waa_drop_total_bps_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0]
waa_delay_total_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 4.1305724590590193e-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.210899904677303e-07, 4.267529781794294e-07, 4.388461266149118e-07, 4.517500780099345e-07, 4.6178750488705807e-07]
waa_delay_high_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
waa_delay_med_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 4.658953752207307e-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.0243350433115525e-07, 4.080269328947565e-07, 4.162545419234789e-07, 4.2472827441108855e-07, 4.2704660518395546e-07]
waa_delay_low_avg_INTER_3200=[0, 0, 0, 0, 0, 0, 0, 0, 3.9539744332741635e-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.695656544669994e-07, 4.6806239554387925e-07, 4.848910338215696e-07, 5.008646946627315e-07, 5.110986788071678e-07]

waa_load_total_bps_avg_E2E_3200=[0.0, 0, 0, 0, 0, 0, 0, 6063851428571.428, 6756220154385.964, 7499773683116.882, 8283452413793.103, 9088910650602.41, 9888380412121.213, 10742325292307.691, 11648730181818.182, 12516342399999.998, 13248745371428.57, 14257673199999.998, 15326692799999.998, 15662857599999.998, 16875401599999.998, 0, 0, 19231924800000.0, 29783119599999.996]
waa_thru_total_bps_avg_E2E_3200=[3217510399999.9995, 0, 0, 0, 0, 0, 0, 6374309257142.856, 6686909024561.402, 6808355999999.999, 6947211944827.585, 7097044125301.204, 7176509624242.423, 7260573784615.384, 7287825163636.362, 7308749439999.999, 7317941942857.142, 7324633199999.999, 7302219199999.999, 7319055999999.999, 7329547199999.999, 0, 0, 7330548799999.999, 7292635599999.999]
waa_drop_total_bps_avg_E2E_3200=[0.0, 0, 0, 0, 0, 0, 0, 370061714285.7143, 655442947368.421, 921529070129.87, 1369838068965.517, 2065983363855.4216, 2789212557575.7573, 3715459815384.6147, 4197278109090.9087, 4874692160000.0, 5070736457142.857, 5277163200000.0, 7031506399999.999, 6636390399999.999, 7853497599999.999, 0, 0, 7195683199999.999, 5084611199999.999]
waa_delay_total_avg_E2E_3200=[0, 0, 0, 0, 0, 0, 0, 8.131291939102018e-06, 1.3122706907744054e-05, 1.8486761670611675e-05, 2.6742806801795815e-05, 4.058823223911778e-05, 5.607194057510249e-05, 7.188159538470969e-05, 9.017629874643822e-05, 9.741000046567237e-05, 9.910836960932806e-05, 9.540676649864983e-05, 9.474334376504136e-05, 0.0001043282882349388, 9.737149713411443e-05, 0, 0, 0.00011198064402933127, 0.0001233266758099803]
waa_delay_high_avg_E2E_3200=[0, 0, 0, 0, 0, 0, 0, 3.407821950242591e-07, 3.4359729914806996e-07, 3.5361158921527003e-07, 3.6805321652934655e-07, 3.8641903074480673e-07, 4.0393149693124064e-07, 4.221653964134396e-07, 4.4200159178697647e-07, 4.480614734608028e-07, 4.5973779186497617e-07, 4.6276684204129025e-07, 4.717559361655054e-07, 4.7403254271946526e-07, 4.7132474620051967e-07, 0, 0, 4.693139333191285e-07, 4.7060410515048494e-07]
waa_delay_med_avg_E2E_3200=[0, 0, 0, 0, 0, 0, 0, 2.1211957430698905e-05, 3.69620513006679e-05, 5.277550648039058e-05, 8.228418042057021e-05, 0.00013969711578978186, 0.0002097154770018747, 0.00027356532968694715, 0.00031706606864403855, 0.00034057933696677396, 0.00029554300823913095, 0.00023965976014248406, 0.00024680935875713746, 0.00026547522161904537, 0.00016893049141332122, 0, 0, 0.00015209755196946435, 7.94615873464541e-05]
waa_delay_low_avg_E2E_3200=[0, 0, 0, 0, 0, 0, 0, 0.00010044597828115594, 0.00013573464200394017, 0.000143341545297473, 0.0001671522885515281, 0.0002100049687469657, 0.000257504161376316, 0.00030889736482909655, 0.0003852020655251942, 0.00038771391308438597, 0.0004168049637663767, 0.000393277863913308, 0.00041572964228173907, 0.00040711479887680784, 0.0004841065784610378, 0, 0, 0.0003927527760826218, 0.00033085578499029517]


def clean_load_thru(load,thru,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/cleaning_factor for i in selected_i]
    thru.insert(0,0)
    return load,thru
def clean_load_thru_drop(load,thru,drop,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            if thru[i] > load[i]:
                thru[i]=load[i]
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)
    thru = [thru[i]/cleaning_factor for i in selected_i]
    thru.insert(0,0)
    drop = [drop[i]/cleaning_factor for i in selected_i]
    drop.insert(0,0)
    return load,thru,drop
def clean_load_delays(load,avg,high,med,low,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)

    avg = [avg[i]*1e3 for i in selected_i]
    avg.insert(0,avg[0])
    high = [high[i]*1e3 for i in selected_i]
    high.insert(0,high[0])
    med = [med[i]*1e3 for i in selected_i]
    med.insert(0,med[0])
    low = [low[i]*1e3 for i in selected_i]
    low.insert(0,low[0])

    return load,avg,high,med,low



def plot_thru_intra(data):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra traffic load (Gbps)'

    if data==2400:
        max_thru=400
        x_lim_begin = 1.95
        #x_lim_end=10
    else:
        max_thru = 600
        x_lim_begin = -10
        x_lim_end = 855

    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads
    if data==2400:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_INTRA_2400, waa_thru_total_bps_avg_INTRA_2400,
                                                waa_drop_total_bps_avg_INTRA_2400,cleaning_factor=1e9)
    elif data==3200:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_INTRA_3200, waa_thru_total_bps_avg_INTRA_3200,
                                                waa_drop_total_bps_avg_INTRA_3200,cleaning_factor=1e9)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def plot_thru_inter(data):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter traffic load (Gbps)'

    if data==2400:
        max_thru=16*4*40
        x_lim_begin = 1.95
        #x_lim_end=10
    else:
        max_thru = 16*4*40
        x_lim_begin = -10
        x_lim_end = 1400

    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads
    if data==2400:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_INTER_2400, waa_thru_total_bps_avg_INTER_2400,
                                                waa_drop_total_bps_avg_INTER_2400,cleaning_factor=1e9)
    elif data==3200:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_INTER_3200, waa_thru_total_bps_avg_INTER_3200,
                                                waa_drop_total_bps_avg_INTER_3200,cleaning_factor=1e9)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def plot_thru_e2e(data):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'

    x_lim_begin=1.95
    if data==2400:
        max_thru=16*0.400
        x_lim_end=10
    else:
        x_lim_end = 15.1
        max_thru = 16 * 0.600

    y_label='Bitrate (Tbps)'
    legend_loc='lower right'

    # Clean my loads
    if data==2400:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_E2E_2400, waa_thru_total_bps_avg_E2E_2400,
                                                waa_drop_total_bps_avg_E2E_2400,cleaning_factor=1e12)
    elif data==3200:
        load, thru, drop = clean_load_thru_drop(waa_load_total_bps_avg_E2E_3200, waa_thru_total_bps_avg_E2E_3200,
                                                waa_drop_total_bps_avg_E2E_3200,cleaning_factor=1e12)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=30
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal throughput", linewidth=_LINEWIDTH)
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()


def plot_delays(data):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'

    x_lim_begin=1.95
    if data==2400:
        x_lim_end=10
    else:
        x_lim_end = 15.1

    y_label='End-to-end delay (ms)'
    legend_loc='center right'

    # Clean my loads
    # Clean my loads
    if data==2400:
        load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_load_total_bps_avg_E2E_2400,
                                                                              waa_delay_total_avg_E2E_2400, waa_delay_high_avg_E2E_2400,
                                                                              waa_delay_med_avg_E2E_2400, waa_delay_low_avg_E2E_2400,cleaning_factor=1e12)

    elif data==3200:
        load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_load_total_bps_avg_E2E_3200,
                                                                              waa_delay_total_avg_E2E_3200, waa_delay_high_avg_E2E_3200,
                                                                              waa_delay_med_avg_E2E_3200, waa_delay_low_avg_E2E_3200,cleaning_factor=1e12)

    print(str(load))
    print(str(high_delay))
    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    ax1.semilogy(load[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
    ax1.semilogy(load[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
    ax1.semilogy(load[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)
    #ax1.semilogy(load[limit:], avg_delay[limit:], 'k', label="avg", linewidth=4)

    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc=legend_loc, fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()

def plot_compare_delay_bar():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total traffic load (Tbps)'

    x_lim_begin=-2
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2.5,5,7.5,10]
    high2400=[0.00045,0.00045,0.00050,0.00056]
    med2400=[0.228,0.234,0.517,0.6]
    low2400=[0.353,0.318,0.483,0.574]
    avg2400=[0.046,0.048,0.111,0.17]
    high3200=[0.00034,0.00034,0.00035,0.00041]
    med3200=[0.021,0.021,0.054,0.22]
    low3200=[0.102,0.102,0.145,0.27]
    avg3200=[0.0082,0.0082,0.019,0.06]

    mini_size = 0.16
    big_size = 0.65
    width = 0.25

    x_med = load
    x_med_2400 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high = [x - big_size for x in x_med]
    x_high_2400 = [x - mini_size for x in x_high]
    x_high_3200  = [x + mini_size for x in x_high]

    x_low = [x + big_size for x in x_med]
    x_low_2400 = [x - mini_size for x in x_low]
    x_low_3200  = [x + mini_size for x in x_low]


    ax1.bar(x_high_2400, high2400, color='white',edgecolor='red', label="High-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_med_2400, med2400,  color='white',edgecolor='green', label="Med-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_low_2400, low2400,  color='white',edgecolor='blue', label="Low-4ch",linewidth=4, width=width,hatch='//')
    ax1.bar(x_high_3200, high3200, color='white',edgecolor='red',  label="High-6ch",linewidth=4, width=width, hatch='o')
    ax1.bar(x_med_3200, med3200, color='white',edgecolor='green', label="Med-6ch",linewidth=4, width=width, hatch='o')
    ax1.bar(x_low_3200, low3200, color='white',edgecolor='blue', label="Low-6ch",linewidth=4, width=width, hatch='o')
    ax1.set_xticks([0,2.5,5,7.5,10])
    legend_fontsize = 21
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=37
    _TICK_PARAMS=45
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_xlim(x_lim_begin,x_lim_end)
    except:
        pass
    try:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    except:
        ax1.legend(loc='upper left', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)

    plt.show()


plot_thru_intra(data=3200)
plot_thru_inter(data=3200)
plot_delays(data=3200)
plot_compare_delay_bar()