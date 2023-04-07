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


def plot_calabr_comparison(dt):
    load_small_go = [0, 2.1167344355555557, 2.401646682352941, 2.7839736084210527, 3.1905813866666666, 3.64618, 4.0436944,
                  4.82793504, 9.49960992]
    thru_small_go = [0, 2.1167344355555557, 2.3995506196078433, 2.781502450526316, 3.1905813866666666, 3.64618, 4.0436944,
                  4.82793504, 7.22758592]
    drop_small_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00121024, 0.00240512]
    avg_delay_small_go = [0, 0.0010642301946057725, 0.0012549515392876207, 0.0016696329093696077, 0.001895897644783818,
                       0.002578142654955094, 0.002519420990169071, 0.010730670059236638, 0.023157451332561217]
    high_delay_small_go = [0, 0.0003915167694499143, 0.00040543632810523207, 0.0004281020019097491, 0.00045004595706244665,
                        0.0005015144836709432, 0.0005106383176940969, 0.0007713113087524994, 0.001072533882210542]
    med_delay_small_go = [0, 0.0005071545022703347, 0.0005147637126791621, 0.0005273426939093233, 0.0005387581926120946,
                       0.0006147577164593574, 0.0005828609440703036, 0.0013740417999102581, 0.0050370303204835725]
    low_delay_small_go = [0, 0.007254209968817725, 0.007279361460422012, 0.008121911784319853, 0.007847691271084875,
                       0.010110772214995605, 0.008080560864905448, 0.03276652937004465, 0.04480355583705122]
    drop_prob_avg_small_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0002506744581219552, 0.0002531809221909609]
    drop_prob_high_small_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_med_small_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_low_small_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004004992368064517, 0.00033538203744498506]

    load_big_go = [0, 3.56470448, 4.110936044137931, 4.6338470704761905, 5.216873687272727, 5.980397165714286, 6.70448736,
                7.27353536, 8.70120832, 15.9186064]
    thru_big_go = [0, 3.56470448, 4.110936044137931, 4.629386278095239, 5.216873687272727, 5.980397165714286, 6.70448736,
                7.05638512, 7.26272896, 7.2425328]
    drop_big_go = [0, 0.0, 0.007860215172413794, 0.012735946666666666, 0.04082484363636364, 0.13266029714285715,
                0.45615128, 0.59142064, 0.57610688, 0.20502304]
    avg_delay_big_go = [0, 0.001998737451705892, 0.0026169308481453196, 0.004237960496907031, 0.008016617735346173,
                     0.020002269728590892, 0.03991414870378548, 0.051748469212839675, 0.07104305784827444,
                     0.06991364330009094]
    high_delay_big_go = [0, 0.0004760464026617077, 0.0005131505584207702, 0.000552638130699876, 0.0006252225402213822,
                      0.0007712728678326273, 0.0009114324392679544, 0.0009525032589449076, 0.0010247328655446054,
                      0.0010392769654492936]
    med_delay_big_go = [0, 0.0006870162827571204, 0.0007644470817997862, 0.00092224740518302, 0.002045116034967567,
                     0.0064554330469916805, 0.01589564735623976, 0.02193482183783836, 0.03352690364689501,
                     0.026745559802776427]
    low_delay_big_go = [0, 0.021136503556269358, 0.02247626764590647, 0.02939864337794904, 0.04624940598229325,
                     0.0981751046134783, 0.1852180044222823, 0.21330960281870656, 0.23708807425403794,
                     0.1424733721831661]
    drop_prob_avg_big_go = [0, 0.0, 0.0018845018026926721, 0.0026757456321793403, 0.007754191594506337,
                         0.021877757991385395, 0.06733521166041224, 0.08095137309762394, 0.09620998587929453,
                         0.01287945909636914]
    drop_prob_high_big_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_med_big_go = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_low_big_go = [0, 0.0, 0.0058045508361986966, 0.0067566351848088665, 0.0170543419050757, 0.042486028824093636,
                         0.12625807777485995, 0.14100250185161212, 0.10607475834319105, 0.01702397248007625]

    load_small_stay = [0, 2.0741661217391303, 2.384309913846154, 2.7438680228571433, 3.1347336, 3.6628901333333337,
                       4.07866384, 4.54757184, 5.37944512, 9.93513952]
    thru_small_stay = [0, 2.0741661217391303, 2.384309913846154, 2.724025142857143, 3.1347336, 3.6628901333333337,
                       4.07866384, 4.54757184, 5.37944512, 7.16864256]
    drop_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01096672, 0.0]
    avg_delay_small_stay = [0, 0.0008339012023784865, 0.001078873516442142, 0.001402328616941769, 0.001755143747235335,
                            0.002015132464525008, 0.004999789474653397, 0.009134282871767744, 0.01701023108832551,
                            0.026855406863892775]
    high_delay_small_stay = [0, 0.00023041307412606223, 0.000231663743558516, 0.00023294012175682495,
                             0.00023676676384188562, 0.00024134592151278374, 0.0002447109475922321,
                             0.000268974332782962, 0.00033097709779068564, 0.0004384229119650156]
    med_delay_small_stay = [0, 0.0005183828009049543, 0.0005287588299670531, 0.0005404311980430471,
                            0.000568659472931176, 0.0006079325694201046, 0.0006917480827953826, 0.0009249521329623095,
                            0.0023387120995493637, 0.005562330527022835]
    low_delay_small_stay = [0, 0.006264128039067243, 0.006753865691540464, 0.007435275133862714, 0.007731475160118122,
                            0.007535359761950987, 0.01835809328220478, 0.029765724099510744, 0.048398142284536094,
                            0.05080969698915852]
    drop_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01096672, 0.0]
    drop_prob_avg_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0020386340515357836, 0.0]
    drop_prob_high_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_med_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_low_small_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003106370929204727, 0.0]

    load_big_stay = [0, 4.0681744951351355, 4.573822220487805, 5.232789942857143, 6.06300752, 6.65102512, 7.26259584,
                     7.88887424, 8.47275424, 9.0114848, 16.7195648]
    thru_big_stay = [0, 4.0681744951351355, 4.55967296, 5.232789942857143, 6.06300752, 6.65102512, 6.98941088,
                     7.0813808, 7.19565856, 7.2024816, 7.1731296]
    drop_big_stay = [0, 0.0017099243243243244, 0.007129108292682927, 0.10097174857142857, 0.19143098666666666,
                     0.67058688, 0.68871808, 0.8168208, 0.75104448, 0.56349088, 0.23789856]
    avg_delay_big_stay = [0, 0.0022614819534698097, 0.0035039392619543456, 0.014835211566942572, 0.024895243716812447,
                          0.045949192550082084, 0.06094022116211189, 0.06905567607120142, 0.07730594337130474,
                          0.0820892894024645, 0.07999232834855952]
    high_delay_big_stay = [0, 0.00025316804104527066, 0.00025988981170315366, 0.0002954131489268143,
                           0.0003232565747834915, 0.0003779302858337804, 0.00040887387950110126, 0.00043207493875430184,
                           0.0004578503514491859, 0.0004625841046126164, 0.0004756819854969705]
    med_delay_big_stay = [0, 0.0007898628421961044, 0.0008661961217281704, 0.0050021544867727965, 0.008470151886866492,
                          0.017901995855696115, 0.02800059438953789, 0.030445376476474967, 0.03890938664740988,
                          0.03944086059764625, 0.02670403418680058]
    low_delay_big_stay = [0, 0.021261515075759626, 0.026427456964654764, 0.09316691269772294, 0.12820994422938276,
                          0.21671484789818982, 0.25831613945610715, 0.2657991320156002, 0.2771926878095625,
                          0.26829432030656514, 0.16091129456601422]
    drop_big_stay = [0, 0.0017099243243243244, 0.007129108292682927, 0.10097174857142857, 0.19143098666666666,
                     0.67058688, 0.68871808, 0.8168208, 0.75104448, 0.56349088, 0.23789856]
    drop_prob_avg_big_stay = [0, 0.000403500110530233, 0.0015454837014065737, 0.019309651936504087, 0.03149109979613637,
                              0.10074369852192794, 0.09482845140456858, 0.1035408570538957, 0.08864230670757658,
                              0.06253030355219596, 0.014228753131181979]
    drop_prob_high_big_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_med_big_stay = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_low_big_stay = [0, 0.0012547293601418803, 0.004095415989381057, 0.04388594997785827, 0.0629379305819378,
                              0.18398177717691427, 0.16869296682328533, 0.17192863792744142, 0.14686791184298356,
                              0.09983020617902108, 0.018598965168891823]

    load_8nodes_small = [0, 1.003328768, 1.1712003586206896, 1.38698928, 1.62831552, 1.78863384, 2.08423152, 2.38132768, 2.71405472,
            5.55383232]
    thru_8nodes_small = [0, 1.003328768, 1.1712003586206896, 1.38655398, 1.60338528, 1.78863384, 2.0728488, 2.38132768, 2.71405472,
            5.26944896]
    drop_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    avg_delay_8nodes_small = [0, 0.0007571275272616238, 0.0011230387441969554, 0.0014501929708216218, 0.0017418084712140164,
                 0.0018468978022794002, 0.0022374588534855577, 0.002746835145241996, 0.003605260326909408,
                 0.007812623631389529]
    high_delay_8nodes_small = [0, 0.0003240068563427679, 0.00033091157459752617, 0.00033945525383495697, 0.0003521918007852375,
                  0.00035796605563015015, 0.000371018728389458, 0.00038613862586722497, 0.0004125729067779879,
                  0.0006891386099708171]
    med_delay_8nodes_small = [0, 0.00048190219770485616, 0.0004869598501563847, 0.0004902501861870109, 0.0005044124479735387,
                 0.000495778864932447, 0.0005056373313408101, 0.0005132984844562699, 0.0005280332385770095,
                 0.0007962624714061468]
    low_delay_8nodes_small = [0, 0.005758501368660801, 0.007102547217127879, 0.0072217916454084515, 0.006987678128506773,
                 0.007278416372521022, 0.007557522490178, 0.008480301009337929, 0.009667931449392726,
                 0.013830557103214536]
    drop_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_avg_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_high_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_med_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    drop_prob_low_8nodes_small = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # delete last N element from small
    n=-1
    load_small_go = load_small_go[:n]
    thru_small_go = thru_small_go[:n]
    drop_small_go = drop_small_go[:n]
    avg_delay_small_go = avg_delay_small_go[:n]
    high_delay_small_go = high_delay_small_go[:n]
    med_delay_small_go = med_delay_small_go[:n]
    low_delay_small_go = low_delay_small_go[:n]
    drop_prob_avg_small_go = drop_prob_avg_small_go[:n]
    drop_prob_high_small_go = drop_prob_high_small_go[:n]
    drop_prob_med_small_go = drop_prob_med_small_go[:n]
    drop_prob_low_small_go = drop_prob_low_small_go[:n]
    # delete first N element from big
    n=4
    load_big_go = load_big_go[n:]
    thru_big_go = thru_big_go[n:]
    drop_big_go = drop_big_go[n:]
    avg_delay_big_go = avg_delay_big_go[n:]
    high_delay_big_go = high_delay_big_go[n:]
    med_delay_big_go = med_delay_big_go[n:]
    low_delay_big_go = low_delay_big_go[n:]
    drop_prob_avg_big_go = drop_prob_avg_big_go[n:]
    drop_prob_high_big_go = drop_prob_high_big_go[n:]
    drop_prob_med_big_go = drop_prob_med_big_go[n:]
    drop_prob_low_big_go = drop_prob_low_big_go[n:]
    # merge small+big
    load_go=load_small_go+load_big_go
    thru_go = thru_small_go+ thru_big_go
    drop_go = drop_small_go + drop_big_go
    avg_delay_go = avg_delay_small_go + avg_delay_big_go
    high_delay_go = high_delay_small_go + high_delay_big_go
    med_delay_go = med_delay_small_go + med_delay_big_go
    low_delay_go = low_delay_small_go + low_delay_big_go
    drop_prob_avg_go = drop_prob_avg_small_go + drop_prob_avg_big_go
    drop_prob_high_go = drop_prob_high_small_go + drop_prob_high_big_go
    drop_prob_med_go = drop_prob_med_small_go + drop_prob_med_big_go
    drop_prob_low_go = drop_prob_low_small_go + drop_prob_low_big_go

    # delete last N element from small
    n=-1
    load_small_stay = load_small_stay[:n]
    thru_small_stay = thru_small_stay[:n]
    drop_small_stay = drop_small_stay[:n]
    avg_delay_small_stay = avg_delay_small_stay[:n]
    high_delay_small_stay = high_delay_small_stay[:n]
    med_delay_small_stay = med_delay_small_stay[:n]
    low_delay_small_stay = low_delay_small_stay[:n]
    drop_prob_avg_small_stay = drop_prob_avg_small_stay[:n]
    drop_prob_high_small_stay = drop_prob_high_small_stay[:n]
    drop_prob_med_small_stay = drop_prob_med_small_stay[:n]
    drop_prob_low_small_stay = drop_prob_low_small_stay[:n]
    # delete first N element from big
    n=4
    load_big_stay = load_big_stay[n:]
    thru_big_stay = thru_big_stay[n:]
    drop_big_stay = drop_big_stay[n:]
    avg_delay_big_stay = avg_delay_big_stay[n:]
    high_delay_big_stay = high_delay_big_stay[n:]
    med_delay_big_stay = med_delay_big_stay[n:]
    low_delay_big_stay = low_delay_big_stay[n:]
    drop_prob_avg_big_stay = drop_prob_avg_big_stay[n:]
    drop_prob_high_big_stay = drop_prob_high_big_stay[n:]
    drop_prob_med_big_stay = drop_prob_med_big_stay[n:]
    drop_prob_low_big_stay = drop_prob_low_big_stay[n:]
    # merge small+big
    load_stay=load_small_stay+load_big_stay
    thru_stay = thru_small_stay+ thru_big_stay
    drop_stay = drop_small_stay + drop_big_stay
    avg_delay_stay = avg_delay_small_stay + avg_delay_big_stay
    high_delay_stay = high_delay_small_stay + high_delay_big_stay
    med_delay_stay = med_delay_small_stay + med_delay_big_stay
    low_delay_stay = low_delay_small_stay + low_delay_big_stay
    drop_prob_avg_stay = drop_prob_avg_small_stay + drop_prob_avg_big_stay
    drop_prob_high_stay = drop_prob_high_small_stay + drop_prob_high_big_stay
    drop_prob_med_stay = drop_prob_med_small_stay + drop_prob_med_big_stay
    drop_prob_low_stay = drop_prob_low_small_stay + drop_prob_low_big_stay


    # get norm values
    nominal= 8 # tera?
    norm_load_go=[x/nominal for x in load_go]
    norm_thru_go = [x / nominal for x in thru_go]
    norm_load_stay=[x/nominal for x in load_stay]
    norm_thru_stay = [x / nominal for x in thru_stay]

    cal_load=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    cal_thru=[0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.7,0.7,0.7]
    if _comparison_date==2022:
        cal_avg_delay=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,20e-3,45e-3,53e-3] # ms
        cal_drop_prob=[0,0,7e-5,4e-4,1e-3,1.5e-3,2e-3,3e-3,3e-2,7e-2]
    else:
        cal_avg_delay=[7.5e-3,7.5e-3,7.5e-3,7.5e-3,7.5e-3,8e-3,9e-3,12.5e-3,21e-3,29e-3] # ms
        cal_drop_prob=[0,0,0,0,0.007,0.010,0.012,0.025,0.06,0.105]


    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45

    if dt=='thru':
        ax1.plot(norm_load_go, norm_thru_go, 'r', label="Ours_go", linewidth=_LINEWIDTH)
        ax1.plot(norm_load_stay, norm_thru_stay, 'g', label="Ours_stay", linewidth=_LINEWIDTH)
        ax1.plot(cal_load, cal_thru, 'b', label="Calabretta "+str(_comparison_date), linewidth=_LINEWIDTH)
        x_label = 'Normalized Load'
        y_label='Normalized Throughput'
        x_lim_begin, x_lim_end=-0.05,1.05
        legend_loc='lower left'
    elif dt == 'delay':
        ax1.plot(norm_load_go, avg_delay_go, 'r', label="Ours_go", linewidth=_LINEWIDTH)
        ax1.plot(norm_load_stay, avg_delay_stay, 'g', label="Ours_stay", linewidth=_LINEWIDTH)
        ax1.plot(cal_load, cal_avg_delay, 'b', label="Calabretta "+str(_comparison_date), linewidth=_LINEWIDTH)
        x_label='Normalized Load'
        y_label = 'Latency (ms)'
        x_lim_begin, x_lim_end=-0.05,1.05
        legend_loc='lower left'
    elif dt == 'loss':
        ax1.plot(norm_load_go, drop_prob_avg_go, 'r', label="Ours_go", linewidth=_LINEWIDTH)
        ax1.plot(norm_load_stay, drop_prob_avg_stay, 'g', label="Ours_stay", linewidth=_LINEWIDTH)
        ax1.plot(cal_load, cal_drop_prob, 'b', label="Calabretta "+str(_comparison_date), linewidth=_LINEWIDTH)
        x_label = 'Normalized Load'
        y_label = 'Packet Loss'
        x_lim_begin, x_lim_end=-0.05,1.05
        legend_loc='lower left'
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
def clean_load_thru_drop_prob(load,thru,drop,drop_prob_avg,drop_prob_high,drop_prob_med,drop_prob_low,cleaning_factor):
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

    drop_prob_avg = [drop_prob_avg[i] for i in selected_i]
    drop_prob_avg.insert(0,0)

    drop_prob_high = [drop_prob_high[i] for i in selected_i]
    drop_prob_high.insert(0,0)

    drop_prob_med= [drop_prob_med[i] for i in selected_i]
    drop_prob_med.insert(0,0)

    drop_prob_low = [drop_prob_low[i] for i in selected_i]
    drop_prob_low.insert(0,0)

    return load,thru,drop,drop_prob_avg,drop_prob_high,drop_prob_med,drop_prob_low
def clean_load_delays(load,avg,high,med,low,cleaning_factor):
    selected_i=[]
    for i in range(0,len(load)):
        if load[i]!=0:
            selected_i.append(i)

    load = [load[i]/cleaning_factor for i in selected_i]
    load.insert(0,0)

    avg = [avg[i]*1e3 for i in selected_i]
    avg.insert(0,0)
    high = [high[i]*1e3 for i in selected_i]
    high.insert(0,0)
    med = [med[i]*1e3 for i in selected_i]
    med.insert(0,0)
    low = [low[i]*1e3 for i in selected_i]
    low.insert(0,0)

    return load,avg,high,med,low

def plot_thru_intra(data,strategy,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 400
        x_lim_begin = -0.1
        x_lim_end=450
        if strategy=='go':
            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                                   waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_7030_load_total_bps_avg, waa_1600_go_intra_7030_thru_total_bps_avg,
                                                   waa_1600_go_intra_7030_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_6040_load_total_bps_avg, waa_1600_go_intra_6040_thru_total_bps_avg,
                                                   waa_1600_go_intra_6040_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                               waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 400
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                               waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                               waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 400
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                               waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                               waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
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
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def plot_thru_per_server_intra(data,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 400
        num_servers = 16
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                               waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                               waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 400
        num_servers = 24
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                               waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                               waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 400
        num_servers=32
        x_lim_begin = -1
        x_lim_end=450
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                               waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                               waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    # Activate thru/drop averaging
    thru=[x/num_servers for x in thru]
    drop = [x / num_servers for x in drop]

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput per server",linewidth=_LINEWIDTH)
    #ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
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
def plot_thru_per_server_intra_multiple(data_list,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Throughput per server (Gbps)'
    legend_loc='upper left'

    load_list=[]
    thru_list=[]
    drop_list=[]
    serv_list=[]

    for data in data_list:
        # Clean my loads and assign max thru values and limits
        if data==1600:
            max_thru = 400
            num_servers = 16
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_intra_load_total_bps_avg, waa_1600_go_intra_thru_total_bps_avg,
                                                   waa_1600_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_1600_stay_intra_load_total_bps_avg, waa_1600_stay_intra_thru_total_bps_avg,
                                                   waa_1600_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif data==2400:
            max_thru = 400
            num_servers = 24
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_2400_go_intra_load_total_bps_avg, waa_2400_go_intra_thru_total_bps_avg,
                                                   waa_2400_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_2400_stay_intra_load_total_bps_avg, waa_2400_stay_intra_thru_total_bps_avg,
                                                   waa_2400_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)
        elif data==3200:
            max_thru = 400
            num_servers=32
            x_lim_begin = -1
            x_lim_end=450
            if strategy=='go':
                load, thru, drop = clean_load_thru_drop(waa_3200_go_intra_load_total_bps_avg, waa_3200_go_intra_thru_total_bps_avg,
                                                   waa_3200_go_intra_drop_total_bps_avg,cleaning_factor=1e9)
            elif strategy=='stay':
                load, thru, drop = clean_load_thru_drop(waa_3200_stay_intra_load_total_bps_avg, waa_3200_stay_intra_thru_total_bps_avg,
                                                   waa_3200_stay_intra_drop_total_bps_avg,cleaning_factor=1e9)

        load_list.append(load)
        thru_list.append(thru)
        drop_list.append(drop)
        serv_list.append(num_servers)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    # Activate thru/drop averaging
    for i in range(len(serv_list)):
        thru_list[i]=[x/serv_list[i] for x in thru_list[i]]
        drop_list[i] = [x / serv_list[i] for x in drop_list[i]]

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    color=['b','b--','b-.']
    color2 = ['r', 'r--', 'r-.']
    for i in range(len(serv_list)):
        ax1.plot(load_list[i], thru_list[i],color[i], label="N="+str(serv_list[i]),linewidth=_LINEWIDTH)
    #ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"throughput", linewidth=_LINEWIDTH)
    try:
        ax1.set_xlabel(x_label, fontsize=_LABEL_SIZE)
    except:
        pass
    try:
        ax1.set_ylabel(y_label, fontsize=_LABEL_SIZE-9)
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
def plot_delay_multiple(data_list,strategy):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    serv_list=[]

    for data in data_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        if data == 1600:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers=16
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_stay_e2e_load_total_bps_avg,
                    waa_1600_stay_e2e_delay_total_avg,
                    waa_1600_stay_e2e_delay_high_avg,
                    waa_1600_stay_e2e_delay_med_avg,
                    waa_1600_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        elif data == 2400:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers = 24
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_2400_go_e2e_load_total_bps_avg,
                    waa_2400_go_e2e_delay_total_avg,
                    waa_2400_go_e2e_delay_high_avg,
                    waa_2400_go_e2e_delay_med_avg,
                    waa_2400_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_2400_stay_e2e_load_total_bps_avg,
                    waa_2400_stay_e2e_delay_total_avg,
                    waa_2400_stay_e2e_delay_high_avg,
                    waa_2400_stay_e2e_delay_med_avg,
                    waa_2400_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        elif data == 3200:
            x_lim_begin = 1.95
            x_lim_end = 10
            num_servers = 32
            if strategy == 'go':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_3200_go_e2e_load_total_bps_avg,
                    waa_3200_go_e2e_delay_total_avg,
                    waa_3200_go_e2e_delay_high_avg,
                    waa_3200_go_e2e_delay_med_avg,
                    waa_3200_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif strategy == 'stay':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_3200_stay_e2e_load_total_bps_avg,
                    waa_3200_stay_e2e_delay_total_avg,
                    waa_3200_stay_e2e_delay_high_avg,
                    waa_3200_stay_e2e_delay_med_avg,
                    waa_3200_stay_e2e_delay_low_avg,
                    cleaning_factor=1e12)

        load_list.append(load)
        delay_list.append(avg_delay)
        serv_list.append(num_servers)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    color=['b','b--','b-.']
    for i in range(len(serv_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="N="+str(serv_list[i]), linewidth=_LINEWIDTH)

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
def plot_thru_inter(data,strategy,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_load_total_bps_avg,
                                                        waa_1600_go_inter_thru_total_bps_avg,
                                                        waa_1600_go_inter_drop_total_bps_avg, cleaning_factor=1e9)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_7030_load_total_bps_avg, waa_1600_go_inter_7030_thru_total_bps_avg,
                                                   waa_1600_go_inter_7030_drop_total_bps_avg,cleaning_factor=1e9)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_inter_6040_load_total_bps_avg, waa_1600_go_inter_6040_thru_total_bps_avg,
                                                   waa_1600_go_inter_6040_drop_total_bps_avg,cleaning_factor=1e9)

        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_inter_load_total_bps_avg, waa_1600_stay_inter_thru_total_bps_avg,
                                               waa_1600_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==2400:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_inter_load_total_bps_avg, waa_2400_go_inter_thru_total_bps_avg,
                                               waa_2400_go_inter_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_inter_load_total_bps_avg, waa_2400_stay_inter_thru_total_bps_avg,
                                               waa_2400_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
    elif data==3200:
        max_thru = 16 * 4 * 40
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_inter_load_total_bps_avg, waa_3200_go_inter_thru_total_bps_avg,
                                               waa_3200_go_inter_drop_total_bps_avg,cleaning_factor=1e9)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_inter_load_total_bps_avg, waa_3200_stay_inter_thru_total_bps_avg,
                                               waa_3200_stay_inter_drop_total_bps_avg,cleaning_factor=1e9)
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
    ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def plot_drop_prob(data,strategy,setup='16x16'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='Bitrate (Tbps)'
    legend_loc='center right'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy == 'go':
            load, thru, drop, drop_prob_avg, drop_prob_high, drop_prob_med, drop_prob_low= clean_load_thru_drop_prob\
                (waa_1600_go_e2e_load_total_bps_avg, waa_1600_go_e2e_thru_total_bps_avg, waa_1600_go_e2e_drop_total_bps_avg,
                 waa_1600_go_e2e_drop_prob_total_avg, waa_1600_go_e2e_drop_prob_high_avg, waa_1600_go_e2e_drop_prob_med_avg,
                 waa_1600_go_e2e_drop_prob_low_avg,cleaning_factor=1e12)
        elif strategy == 'stay':
            load, thru, drop, drop_prob_avg, drop_prob_high, drop_prob_med, drop_prob_low= clean_load_thru_drop_prob\
                (waa_1600_stay_e2e_load_total_bps_avg, waa_1600_stay_e2e_thru_total_bps_avg, waa_1600_stay_e2e_drop_total_bps_avg,
                 waa_1600_stay_e2e_drop_prob_total_avg, waa_1600_stay_e2e_drop_prob_high_avg, waa_1600_stay_e2e_drop_prob_med_avg,
                 waa_1600_stay_e2e_drop_prob_low_avg,cleaning_factor=1e12)
    elif data==400 and setup=='16x8':
        x_lim_begin = -0.1
        x_lim_end=10
        load, thru, drop, drop_prob_avg, drop_prob_high, drop_prob_med, drop_prob_low= clean_load_thru_drop_prob\
                (waa_400_16x8_go_e2e_load_total_bps_avg, waa_400_16x8_go_e2e_thru_total_bps_avg, waa_400_16x8_go_e2e_drop_total_bps_avg,
                 waa_400_16x8_go_e2e_drop_prob_total_avg, waa_400_16x8_go_e2e_drop_prob_high_avg, waa_400_16x8_go_e2e_drop_prob_med_avg,
                 waa_400_16x8_go_e2e_drop_prob_low_avg,cleaning_factor=1e12)
    elif data==800:
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy == 'go':
            load, thru, drop, drop_prob_avg, drop_prob_high, drop_prob_med, drop_prob_low= clean_load_thru_drop_prob\
                (waa_800_go_e2e_load_total_bps_avg, waa_800_go_e2e_thru_total_bps_avg, waa_800_go_e2e_drop_total_bps_avg,
                 waa_800_go_e2e_drop_prob_total_avg, waa_800_go_e2e_drop_prob_high_avg, waa_800_go_e2e_drop_prob_med_avg,
                 waa_800_go_e2e_drop_prob_low_avg,cleaning_factor=1e12)
        elif strategy == 'stay':
            load, thru, drop, drop_prob_avg, drop_prob_high, drop_prob_med, drop_prob_low= clean_load_thru_drop_prob\
                (waa_800_stay_e2e_load_total_bps_avg, waa_800_stay_e2e_thru_total_bps_avg, waa_800_stay_e2e_drop_total_bps_avg,
                 waa_800_stay_e2e_drop_prob_total_avg, waa_800_stay_e2e_drop_prob_high_avg, waa_800_stay_e2e_drop_prob_med_avg,
                 waa_800_stay_e2e_drop_prob_low_avg,cleaning_factor=1e12)


    print('Drop prob plot, LOAD='+str(load))
    print('Drop prob plot, drop=' + str(drop))
    print('Drop prob plot, drop_prob_avg=' + str(drop_prob_avg))
    print('Drop prob plot, drop_prob_high=' + str(drop_prob_high))
    print('Drop prob plot, drop_prob_med=' + str(drop_prob_med))
    print('Drop prob plot, drop_prob_low=' + str(drop_prob_low))


    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=30
    _TICK_PARAMS=45
    ax1.plot(load, drop_prob_avg,'k', label="Drop Prob Avg",linewidth=_LINEWIDTH)
    ax1.plot(load, drop_prob_high, 'r', label="Drop Prob High", linewidth=_LINEWIDTH)
    ax1.plot(load, drop_prob_med, 'g', label="Drop Prob Med", linewidth=_LINEWIDTH)
    ax1.plot(load, drop_prob_low, 'b', label="Drop Prob Low", linewidth=_LINEWIDTH)
    ax1.set_yscale('symlog')
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
def plot_thru_e2e(data,strategy,distribution='8020',setup='16x16'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='Bitrate (Tbps)'
    legend_loc='center right'

    # Clean my loads and assign max thru values and limits
    if data==1600:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            if distribution=='8020':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_load_total_bps_avg, waa_1600_go_e2e_thru_total_bps_avg,
                                               waa_1600_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
            elif distribution=='7030':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_7030_load_total_bps_avg, waa_1600_go_e2e_7030_thru_total_bps_avg,
                                                   waa_1600_go_e2e_7030_drop_total_bps_avg,cleaning_factor=1e12)
            elif distribution=='6040':
                load, thru, drop = clean_load_thru_drop(waa_1600_go_e2e_6040_load_total_bps_avg, waa_1600_go_e2e_6040_thru_total_bps_avg,
                                                   waa_1600_go_e2e_6040_drop_total_bps_avg,cleaning_factor=1e12)

        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_1600_stay_e2e_load_total_bps_avg, waa_1600_stay_e2e_thru_total_bps_avg,
                                               waa_1600_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==400 and setup=='16x8':
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        load, thru, drop = clean_load_thru_drop(waa_400_16x8_go_e2e_load_total_bps_avg, waa_400_16x8_go_e2e_thru_total_bps_avg,
                                                   waa_400_16x8_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==800:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_800_go_e2e_load_total_bps_avg, waa_800_go_e2e_thru_total_bps_avg,
                                                   waa_800_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_800_stay_e2e_load_total_bps_avg, waa_800_stay_e2e_thru_total_bps_avg,
                                                   waa_800_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==2400:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_2400_go_e2e_load_total_bps_avg, waa_2400_go_e2e_thru_total_bps_avg,
                                               waa_2400_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_2400_stay_e2e_load_total_bps_avg, waa_2400_stay_e2e_thru_total_bps_avg,
                                               waa_2400_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    elif data==3200:
        max_thru = 16*0.4+16*0.1
        x_lim_begin = -0.1
        x_lim_end=10
        if strategy=='go':
            load, thru, drop = clean_load_thru_drop(waa_3200_go_e2e_load_total_bps_avg, waa_3200_go_e2e_thru_total_bps_avg,
                                               waa_3200_go_e2e_drop_total_bps_avg,cleaning_factor=1e12)
        elif strategy=='stay':
            load, thru, drop = clean_load_thru_drop(waa_3200_stay_e2e_load_total_bps_avg, waa_3200_stay_e2e_thru_total_bps_avg,
                                               waa_3200_stay_e2e_drop_total_bps_avg,cleaning_factor=1e12)
    nominal_thru=[]
    for el in load:
        nominal_thru.append(max_thru)

    print('plot_thru_e2e, LOAD='+str(load))
    print('plot_thru_e2e, thru='+str(thru))
    print('plot_thru_e2e, drop='+str(drop))

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=30
    _TICK_PARAMS=45
    ax1.plot(load, thru,'b', label="Throughput",linewidth=_LINEWIDTH)
    ax1.plot(load, drop,'r', label="Drop-rate",linewidth=_LINEWIDTH)
    ax1.plot(load, nominal_thru, 'k--', label="Nominal capacity", linewidth=_LINEWIDTH)
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
def plot_delays_e2e(data, strategy,toplot,distribution='8020',setup='16x16'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600 and setup=='16x16':
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='7030':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_delay_total_avg,
                    waa_1600_go_e2e_7030_delay_high_avg,
                    waa_1600_go_e2e_7030_delay_med_avg,
                    waa_1600_go_e2e_7030_delay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='6040':
                load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_delay_total_avg,
                    waa_1600_go_e2e_6040_delay_high_avg,
                    waa_1600_go_e2e_6040_delay_med_avg,
                    waa_1600_go_e2e_6040_delay_low_avg,
                    cleaning_factor=1e12)

        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_delay_total_avg,
                                                                                  waa_1600_stay_e2e_delay_high_avg,
                                                                                  waa_1600_stay_e2e_delay_med_avg,
                                                                                  waa_1600_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==400 and setup=='16x8':
        x_lim_begin = 1.95
        x_lim_end=10
        load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                waa_400_16x8_go_e2e_load_total_bps_avg,
                waa_400_16x8_go_e2e_delay_total_avg,
                waa_400_16x8_go_e2e_delay_high_avg,
                waa_400_16x8_go_e2e_delay_med_avg,
                waa_400_16x8_go_e2e_delay_low_avg,
                cleaning_factor=1e12)
    elif data==800 and setup=='16x16':
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                waa_800_go_e2e_load_total_bps_avg,
                waa_800_go_e2e_delay_total_avg,
                waa_800_go_e2e_delay_high_avg,
                waa_800_go_e2e_delay_med_avg,
                waa_800_go_e2e_delay_low_avg,
                cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                waa_800_stay_e2e_load_total_bps_avg,
                waa_800_stay_e2e_delay_total_avg,
                waa_800_stay_e2e_delay_high_avg,
                waa_800_stay_e2e_delay_med_avg,
                waa_800_stay_e2e_delay_low_avg,
                cleaning_factor=1e12)
    elif data==2400 and setup=='16x16':
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_delay_total_avg,
                                                                                  waa_2400_go_e2e_delay_high_avg,
                                                                                  waa_2400_go_e2e_delay_med_avg,
                                                                                  waa_2400_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_delay_total_avg,
                                                                                  waa_2400_stay_e2e_delay_high_avg,
                                                                                  waa_2400_stay_e2e_delay_med_avg,
                                                                                  waa_2400_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200 and setup=='16x16':
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_delay_total_avg,
                                                                                  waa_3200_go_e2e_delay_high_avg,
                                                                                  waa_3200_go_e2e_delay_med_avg,
                                                                                  waa_3200_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_delay_total_avg,
                                                                                  waa_3200_stay_e2e_delay_high_avg,
                                                                                  waa_3200_stay_e2e_delay_med_avg,
                                                                                  waa_3200_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)

    print('plot_delays_e2e, LOAD='+str(load))
    print('plot_delays_e2e, avg_delay='+str(avg_delay))
    print('plot_delays_e2e, high_delay='+str(high_delay))
    print('plot_delays_e2e, med_delay='+str(med_delay))
    print('plot_delays_e2e, low_delay='+str(low_delay))

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_delay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
def plot_qdelays_e2e(data, strategy,toplot,distribution='8020'):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end qdelay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':

            if distribution=='8020':
                load, avg_qdelay, high_qdelay, med_delay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_qdelay_total_avg,
                    waa_1600_go_e2e_qdelay_high_avg,
                    waa_1600_go_e2e_qdelay_med_avg,
                    waa_1600_go_e2e_qdelay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='7030':
                load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_qdelay_total_avg,
                    waa_1600_go_e2e_7030_qdelay_high_avg,
                    waa_1600_go_e2e_7030_qdelay_med_avg,
                    waa_1600_go_e2e_7030_qdelay_low_avg,
                    cleaning_factor=1e12)
            elif distribution=='6040':
                load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_qdelay_total_avg,
                    waa_1600_go_e2e_6040_qdelay_high_avg,
                    waa_1600_go_e2e_6040_qdelay_med_avg,
                    waa_1600_go_e2e_6040_qdelay_low_avg,
                    cleaning_factor=1e12)

        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_qdelay, high_qdelay, med_qdelay, low_qdelay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

    print(str(load))
    print(str(high_qdelay))
    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_qdelay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_qdelay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_qdelay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_qdelay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_qdelay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
def plot_qdelays_2e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='Queuing delay (ms)'
    legend_loc='center right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_qdelay_total_avg,
                                                                                  waa_1600_go_e2e_qdelay_high_avg,
                                                                                  waa_1600_go_e2e_qdelay_med_avg,
                                                                                  waa_1600_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

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

    if toplot in ['only_avg','all']:
        ax1.semilogy(load[limit:], avg_delay[limit:], 'k', label="avg", linewidth=4)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
def plot_delays_n_qdelays_e2e(data, strategy,toplot):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='center right'
    y_lim_begin=0
    y_lim_end=1e-1
    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_delay_total_avg,
                                                                                  waa_1600_go_e2e_delay_high_avg,
                                                                                  waa_1600_go_e2e_delay_med_avg,
                                                                                  waa_1600_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_1600_go_e2e_load_total_bps_avg,
                                                                                  waa_1600_go_e2e_qdelay_total_avg,
                                                                                  waa_1600_go_e2e_qdelay_high_avg,
                                                                                  waa_1600_go_e2e_qdelay_med_avg,
                                                                                  waa_1600_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_delay_total_avg,
                                                                                  waa_1600_stay_e2e_delay_high_avg,
                                                                                  waa_1600_stay_e2e_delay_med_avg,
                                                                                  waa_1600_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_1600_stay_e2e_load_total_bps_avg,
                                                                                  waa_1600_stay_e2e_qdelay_total_avg,
                                                                                  waa_1600_stay_e2e_qdelay_high_avg,
                                                                                  waa_1600_stay_e2e_qdelay_med_avg,
                                                                                  waa_1600_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==2400:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_delay_total_avg,
                                                                                  waa_2400_go_e2e_delay_high_avg,
                                                                                  waa_2400_go_e2e_delay_med_avg,
                                                                                  waa_2400_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_2400_go_e2e_load_total_bps_avg,
                                                                                  waa_2400_go_e2e_qdelay_total_avg,
                                                                                  waa_2400_go_e2e_qdelay_high_avg,
                                                                                  waa_2400_go_e2e_qdelay_med_avg,
                                                                                  waa_2400_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_delay_total_avg,
                                                                                  waa_2400_stay_e2e_delay_high_avg,
                                                                                  waa_2400_stay_e2e_delay_med_avg,
                                                                                  waa_2400_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_2400_stay_e2e_load_total_bps_avg,
                                                                                  waa_2400_stay_e2e_qdelay_total_avg,
                                                                                  waa_2400_stay_e2e_qdelay_high_avg,
                                                                                  waa_2400_stay_e2e_qdelay_med_avg,
                                                                                  waa_2400_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
    elif data==3200:
        #    x_lim_begin = 1.95
        #    x_lim_end=10
        if strategy=='go':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_delay_total_avg,
                                                                                  waa_3200_go_e2e_delay_high_avg,
                                                                                  waa_3200_go_e2e_delay_med_avg,
                                                                                  waa_3200_go_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_3200_go_e2e_load_total_bps_avg,
                                                                                  waa_3200_go_e2e_qdelay_total_avg,
                                                                                  waa_3200_go_e2e_qdelay_high_avg,
                                                                                  waa_3200_go_e2e_qdelay_med_avg,
                                                                                  waa_3200_go_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)
        elif strategy=='stay':
            load_delay, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_delay_total_avg,
                                                                                  waa_3200_stay_e2e_delay_high_avg,
                                                                                  waa_3200_stay_e2e_delay_med_avg,
                                                                                  waa_3200_stay_e2e_delay_low_avg,
                                                                                  cleaning_factor=1e12)
            load_q, avg_q, high_q, med_q, low_q = clean_load_delays(waa_3200_stay_e2e_load_total_bps_avg,
                                                                                  waa_3200_stay_e2e_qdelay_total_avg,
                                                                                  waa_3200_stay_e2e_qdelay_high_avg,
                                                                                  waa_3200_stay_e2e_qdelay_med_avg,
                                                                                  waa_3200_stay_e2e_qdelay_low_avg,
                                                                                  cleaning_factor=1e12)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load_delay[limit:], avg_delay[limit:], 'b', label="total delay", linewidth=_LINEWIDTH+1)
        ax1.semilogy(load_q[limit:], avg_q[limit:], 'r', label="queuing delay", linewidth=_LINEWIDTH)
    if toplot in ['only_hml','all']:
        ax1.semilogy(load_delay[limit:], high_delay[limit:],'r', label="High",linewidth=_LINEWIDTH)
        ax1.semilogy(load_delay[limit:], med_delay[limit:],'g', label="Med",linewidth=_LINEWIDTH)
        ax1.semilogy(load_delay[limit:], low_delay[limit:],'b', label="Low",linewidth=_LINEWIDTH)

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
        ax1.set_ylim(y_lim_begin,y_lim_end)
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

    x_label='Total load (Tbps)'

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
def plot_compare_delay_bar_B():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-2
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2,4,6,8,10]
    high_go=[0.000476,0.000506,0.000777,0.000989,0.00103]
    med_go = [0.000685,0.000748,0.0066,0.0272,0.0322]
    low_go = [0.0211,0.0222,0.1,0.225,0.237]
    high_stay=[0.000253,0.000253,0.000321,0.000437,0.000464]
    med_stay = [0.00079,0.00079,0.00814,0.0318,0.0382]
    low_stay = [0.0213,0.024,0.125,0.266,0.277]

    for i in range(0,len(load)):
        hh=(100*(high_go[i]-high_stay[i]))/high_go[i]
        mm = (100 * (med_go[i] - med_stay[i])) / med_go[i]
        ll = (100 * (low_go[i] - low_stay[i])) / low_go[i]
        print('Load='+str(load[i]))
        print('high change='+str(hh))
        print('med change=' + str(mm))
        print('low change=' + str(ll))
        print('----')

    mini_size = 0.14
    big_size = 0.55
    width = 0.2

    x_med = load
    x_med_2400 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high = [x - big_size for x in x_med]
    x_high_2400 = [x - mini_size for x in x_high]
    x_high_3200  = [x + mini_size for x in x_high]

    x_low = [x + big_size for x in x_med]
    x_low_2400 = [x - mini_size for x in x_low]
    x_low_3200  = [x + mini_size for x in x_low]


    ax1.bar(x_high_2400, high_go, color='white',edgecolor='red', label="Vanilla/High",linewidth=4, width=width,hatch='//')
    ax1.bar(x_med_2400, med_go,  color='white',edgecolor='green', label="Vanilla/Med",linewidth=4, width=width,hatch='//')
    ax1.bar(x_low_2400, low_go,  color='white',edgecolor='blue', label="Vanilla/Low",linewidth=4, width=width,hatch='//')
    ax1.bar(x_high_3200, high_stay, color='white',edgecolor='red',  label="StayIn/Low",linewidth=4, width=width, hatch='o')
    ax1.bar(x_med_3200, med_stay, color='white',edgecolor='green', label="StayIn/Med",linewidth=4, width=width, hatch='o')
    ax1.bar(x_low_3200, low_stay, color='white',edgecolor='blue', label="StayIn/High",linewidth=4, width=width, hatch='o')
    ax1.set_xticks([2,4,6,8,10])

    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=33
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
def plot_compare_delay_bar_C():
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'

    x_lim_begin=-3
    x_lim_end=12
    y_label='End-to-end delay (ms)'
    legend_loc='lower left'

    fig, ax1 = plt.subplots(constrained_layout=False)
    ax1.set_yscale('log')

    load=[2,4,6,8,10]
#    high_1600= [0.000256,0.000256,0.000320,0.000440,0.000460]
#    med_1600 = [0.000800,0.000800,0.000830,0.033700,0.033800]
#    low_1600 = [0.021700,0.021700,0.128000,0.275000,0.288000]

    high_1600=[0.000253,0.000253,0.000321,0.000437,0.000464]
    med_1600 = [0.00079,0.00079,0.00814,0.0318,0.0382]
    low_1600 = [0.0213,0.024,0.125,0.266,0.277]

    high_2400= [0.0160,0.0160,0.0220,0.111,0.117]
    med_2400 = [0.0629,0.0629,0.0784,0.317,0.636]
    low_2400 = [0.1040,0.1040,0.1290,0.459,0.827]

    high_3200= [0.044,0.044,0.048,0.122,0.126]
    med_3200 = [0.089,0.089,0.100,0.362,0.772]
    low_3200 = [0.149,0.149,0.159,0.504,0.844]


    for i in range(0,len(load)):
        #hh_24=(100*(high_2400[i]-high_1600[i]))/high_1600[i]
        #hh_32 = (100 * (high_3200[i] - high_1600[i])) / high_1600[i]

        #mm_24=(100*(med_2400[i]-med_1600[i]))/med_1600[i]
        #mm_32 = (100 * (med_3200[i] - med_1600[i])) / med_1600[i]

        #ll_24=(100*(low_2400[i]-low_1600[i]))/low_1600[i]
        #ll_32 = (100 * (low_3200[i] - low_1600[i])) / low_1600[i]

        hh_24=(1*(high_2400[i]-0))/high_1600[i]
        hh_32 = (1 * (high_3200[i] - 0)) / high_1600[i]

        mm_24=(1*(med_2400[i]-0))/med_1600[i]
        mm_32 = (1 * (med_3200[i] - 0)) / med_1600[i]

        ll_24=(1*(low_2400[i]-0))/low_1600[i]
        ll_32 = (1 * (low_3200[i] - 0)) / low_1600[i]

        print('Load='+str(load[i]))
        print('high_24='+str(hh_24))
        print('high_32=' + str(hh_32))

        print('med_24='+str(mm_24))
        print('med_32=' + str(mm_32))

        print('low_24='+str(ll_24))
        print('low_32=' + str(ll_32))

        print('----')

    mini_size = 0.2
    big_size = 0.58
    width = 0.12

    x_med=load
    x_med_2400=x_med
    x_med_1600 = [x - mini_size for x in x_med]
    x_med_3200 = [x + mini_size for x in x_med]

    x_high_2400 = [x - big_size for x in x_med]
    x_high_1600 = [x - mini_size for x in x_high_2400]
    x_high_3200  = [x + mini_size for x in x_high_2400]

    x_low_2400 = [x + big_size for x in x_med]
    x_low_1600 = [x - mini_size for x in x_low_2400]
    x_low_3200  = [x + mini_size for x in x_low_2400]

    ax1.bar(x_high_1600, high_1600, color='white',edgecolor='red', label="High-16",linewidth=4, width=width,hatch='/')
    ax1.bar(x_med_1600, med_1600,  color='white',edgecolor='green', label="Med-16",linewidth=4, width=width,hatch='/')
    ax1.bar(x_low_1600, low_1600,  color='white',edgecolor='blue', label="Low-16",linewidth=4, width=width,hatch='/')

    ax1.bar(x_high_2400, high_2400, color='white',edgecolor='red', label="High-24",linewidth=4, width=width,hatch='.')
    ax1.bar(x_med_2400, med_2400,  color='white',edgecolor='green', label="Med-24",linewidth=4, width=width,hatch='.')
    ax1.bar(x_low_2400, low_2400,  color='white',edgecolor='blue', label="Low-24",linewidth=4, width=width,hatch='.')

    ax1.bar(x_high_3200, high_3200, color='white',edgecolor='red', label="High-32",linewidth=4, width=width,hatch='+')
    ax1.bar(x_med_3200, med_3200,  color='white',edgecolor='green', label="Med-32",linewidth=4, width=width,hatch='+')
    ax1.bar(x_low_3200, low_3200,  color='white',edgecolor='blue', label="Low-32",linewidth=4, width=width,hatch='+')

    ax1.set_xticks([2,4,6,8,10])

    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=33
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
def plot_delay_comparison(data=1600, strategy='go',toplot='only_avg',dist_list=['8020','7030','6040']):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Total load (Tbps)'
    y_label='End-to-end delay (ms)'
    legend_loc='lower right'

    # Clean my loads and assign limits
    if data==1600:
        x_lim_begin = 1.95
        x_lim_end=10
        if strategy=='go':
                load_6040, avg_delay_6040, high_delay_6040, med_delay_6040, low_delay_6040 = clean_load_delays(
                    waa_1600_go_e2e_6040_load_total_bps_avg,
                    waa_1600_go_e2e_6040_delay_total_avg,
                    waa_1600_go_e2e_6040_delay_high_avg,
                    waa_1600_go_e2e_6040_delay_med_avg,
                    waa_1600_go_e2e_6040_delay_low_avg,
                    cleaning_factor=1e12)
                load_7030, avg_delay_7030, high_delay_7030, med_delay_7030, low_delay_7030 = clean_load_delays(
                    waa_1600_go_e2e_7030_load_total_bps_avg,
                    waa_1600_go_e2e_7030_delay_total_avg,
                    waa_1600_go_e2e_7030_delay_high_avg,
                    waa_1600_go_e2e_7030_delay_med_avg,
                    waa_1600_go_e2e_7030_delay_low_avg,
                    cleaning_factor=1e12)
                load_8020, avg_delay_8020, high_delay_8020, med_delay_8020, low_delay_8020 = clean_load_delays(
                    waa_1600_go_e2e_load_total_bps_avg,
                    waa_1600_go_e2e_delay_total_avg,
                    waa_1600_go_e2e_delay_high_avg,
                    waa_1600_go_e2e_delay_med_avg,
                    waa_1600_go_e2e_delay_low_avg,
                    cleaning_factor=1e12)
        else:
            pass
    else:
        pass

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=40
    _TICK_PARAMS=45

    if toplot in ['only_avg','all']:
        ax1.semilogy(load_6040[limit:], avg_delay_6040[limit:], 'k', label="intra=60%,inter=40%", linewidth=5,linestyle='dashdot')
        ax1.semilogy(load_7030[limit:], avg_delay_7030[limit:], 'k', label="intra=70%,inter=30%", linewidth=5,linestyle='dashed')
        ax1.semilogy(load_8020[limit:], avg_delay_8020[limit:], 'k', label="intra=80%,inter=20%", linewidth=5,linestyle='solid')

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


def test_plot_stayin_intra_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(intra_8020_load_total_bps_avg, intra_8020_thru_total_bps_avg,
                                                   intra_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(intra_7030_load_total_bps_avg, intra_7030_thru_total_bps_avg,
                                                   intra_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(intra_6040_load_total_bps_avg, intra_6040_thru_total_bps_avg,
                                                   intra_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def test_plot_stayin_intra_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Intra load (Gbps)'
    y_label='Intra delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_8020_load_total_bps_avg,
                    intra_8020_delay_total_avg,
                    intra_8020_delay_high_avg,
                    intra_8020_delay_med_avg,
                    intra_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_7030_load_total_bps_avg,
                    intra_7030_delay_total_avg,
                    intra_7030_delay_high_avg,
                    intra_7030_delay_med_avg,
                    intra_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    intra_6040_load_total_bps_avg,
                    intra_6040_delay_total_avg,
                    intra_6040_delay_high_avg,
                    intra_6040_delay_med_avg,
                    intra_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
def test_plot_stayin_inter_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter-rack load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    #x_lim_begin = -0.1
    #x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(inter_8020_load_total_bps_avg, inter_8020_thru_total_bps_avg,
                                                   inter_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(inter_7030_load_total_bps_avg, inter_7030_thru_total_bps_avg,
                                                   inter_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(inter_6040_load_total_bps_avg, inter_6040_thru_total_bps_avg,
                                                   inter_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def test_plot_stayin_inter_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='Inter load (Gbps)'
    y_label='Inter delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        #x_lim_begin = 0
        #x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_8020_load_total_bps_avg,
                    inter_8020_delay_total_avg,
                    inter_8020_delay_high_avg,
                    inter_8020_delay_med_avg,
                    inter_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_7030_load_total_bps_avg,
                    inter_7030_delay_total_avg,
                    inter_7030_delay_high_avg,
                    inter_7030_delay_med_avg,
                    inter_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    inter_6040_load_total_bps_avg,
                    inter_6040_delay_total_avg,
                    inter_6040_delay_high_avg,
                    inter_6040_delay_med_avg,
                    inter_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
def test_plot_stayin_brul_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON UL load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    #max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 2000

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(brul_8020_load_total_bps_avg, brul_8020_thru_total_bps_avg,
                                                   brul_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(brul_7030_load_total_bps_avg, brul_7030_thru_total_bps_avg,
                                                   brul_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(brul_6040_load_total_bps_avg, brul_6040_thru_total_bps_avg,
                                                   brul_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def test_plot_stayin_brul_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON UL load (Gbps)'
    y_label='PON UL load delay (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 2000
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_8020_load_total_bps_avg,
                    brul_8020_delay_total_avg,
                    brul_8020_delay_high_avg,
                    brul_8020_delay_med_avg,
                    brul_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_7030_load_total_bps_avg,
                    brul_7030_delay_total_avg,
                    brul_7030_delay_high_avg,
                    brul_7030_delay_med_avg,
                    brul_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brul_6040_load_total_bps_avg,
                    brul_6040_delay_total_avg,
                    brul_6040_delay_high_avg,
                    brul_6040_delay_med_avg,
                    brul_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
def test_plot_stayin_brdl_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON DL load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    #x_lim_begin = -0.1
    #x_lim_end = 450

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(brdl_8020_load_total_bps_avg, brdl_8020_thru_total_bps_avg,
                                                   brdl_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(brdl_7030_load_total_bps_avg, brdl_7030_thru_total_bps_avg,
                                                   brdl_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(brdl_6040_load_total_bps_avg, brdl_6040_thru_total_bps_avg,
                                                   brdl_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def test_plot_stayin_brdl_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='PON DL  (Gbps)'
    y_label='PON DL  (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        #x_lim_begin = 0
        #x_lim_end = 400
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_8020_load_total_bps_avg,
                    brdl_8020_delay_total_avg,
                    brdl_8020_delay_high_avg,
                    brdl_8020_delay_med_avg,
                    brdl_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_7030_load_total_bps_avg,
                    brdl_7030_delay_total_avg,
                    brdl_7030_delay_high_avg,
                    brdl_7030_delay_med_avg,
                    brdl_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    brdl_6040_load_total_bps_avg,
                    brdl_6040_delay_total_avg,
                    brdl_6040_delay_high_avg,
                    brdl_6040_delay_med_avg,
                    brdl_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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
def test_plot_stayin_e2e_thru_drop(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='end2end load (Gbps)'
    y_label='Bitrate (Gbps)'
    legend_loc='center left'

    # Clean my loads and assign max thru values and limits
    # data == 1600:
    max_thru = 400
    x_lim_begin = -0.1
    x_lim_end = 8500

    if 8020 in traffic_list:
        load_8020, thru_8020, drop_8020 = clean_load_thru_drop(e2e_8020_load_total_bps_avg, e2e_8020_thru_total_bps_avg,
                                                   e2e_8020_drop_total_bps_avg,cleaning_factor=1e9)
    if 7030 in traffic_list:
        load_7030, thru_7030, drop_7030 = clean_load_thru_drop(e2e_7030_load_total_bps_avg, e2e_7030_thru_total_bps_avg,
                                                   e2e_7030_drop_total_bps_avg,cleaning_factor=1e9)

    if 6040 in traffic_list:
        load_6040, thru_6040, drop_6040 = clean_load_thru_drop(e2e_6040_load_total_bps_avg, e2e_6040_thru_total_bps_avg,
                                                   e2e_6040_drop_total_bps_avg,cleaning_factor=1e9)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
        #nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=28
    _TICK_PARAMS=45
    ax1.plot(load_8020, thru_8020,'b', label="Throughput 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_8020, drop_8020,'r', label="Drop 8020",linewidth=_LINEWIDTH)
    ax1.plot(load_7030, thru_7030,'b', label="Throughput 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_7030, drop_7030,'r', label="Drop 7030",linewidth=_LINEWIDTH,linestyle='dashed')
    ax1.plot(load_6040, thru_6040,'b', label="Throughput 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    ax1.plot(load_6040, drop_6040,'r', label="Drop 6040",linewidth=_LINEWIDTH,linestyle='dotted')
    #ax1.plot(load, nominal_thru, 'k--', label="Nominal"+ "\n"+"capacity", linewidth=_LINEWIDTH)
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
def test_plot_stayin_e2e_delays(traffic_list):
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_label='end2end (Gbps)'
    y_label='end2end  (ms)'
    legend_loc='lower right'

    load_list=[]
    delay_list=[]
    label_list=[]

    for tr in traffic_list:
        # Clean my loads and assign max thru values and limits
        # Clean my loads and assign limits
        #if data == 1600:
        x_lim_begin = 0
        x_lim_end = 8500
        num_servers=16
        mylabel = str(tr)
        if tr==8020:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_8020_load_total_bps_avg,
                    e2e_8020_delay_total_avg,
                    e2e_8020_delay_high_avg,
                    e2e_8020_delay_med_avg,
                    e2e_8020_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==7030:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_7030_load_total_bps_avg,
                    e2e_7030_delay_total_avg,
                    e2e_7030_delay_high_avg,
                    e2e_7030_delay_med_avg,
                    e2e_7030_delay_low_avg,
                    cleaning_factor=1e9)
        elif tr==6040:
            load, avg_delay, high_delay, med_delay, low_delay = clean_load_delays(
                    e2e_6040_load_total_bps_avg,
                    e2e_6040_delay_total_avg,
                    e2e_6040_delay_high_avg,
                    e2e_6040_delay_med_avg,
                    e2e_6040_delay_low_avg,
                    cleaning_factor=1e9)


        load_list.append(load)
        delay_list.append(avg_delay)
        label_list.append(mylabel)

    # Activate max throughput line
    #nominal_thru=[]
    #for el in load:
    #        nominal_thru.append(max_thru)

    fig, ax1 = plt.subplots(constrained_layout=True)
    #ax1.set_yscale('symlog')
    #ax1.plot(load, avg_delay,'k-.', label="Avg",linewidth=4)
    limit=0
    _LINEWIDTH=7
    _LABEL_SIZE=45
    _LEGEND_SIZE=45
    _TICK_PARAMS=45
    print(str(delay_list))
    color=['b','r','g','k','b--','b-.']
    for i in range(len(label_list)):
        ax1.semilogy(load_list[i][limit:], delay_list[i][limit:],color[i], label="perc="+str(label_list[i]), linewidth=_LINEWIDTH)

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

plot_compare_delay_bar_C()

graph_list='scaling'

if graph_list=='basic':
    # Group A: Plots for basic scenario (1600-go)
    plot_thru_intra(data=1600,strategy='go') # data in [1600,2400,3200], strategy in ['go','stay'] #5a
    plot_thru_inter(data=1600,strategy='go') #5b
    plot_thru_e2e(data=1600, strategy='go') #6a
    ###plot_delays_e2e(data=1600, strategy='go',toplot='only_avg')
    ###plot_qdelays_e2e(data=1600, strategy='go',toplot='only_avg')
    plot_delays_n_qdelays_e2e(data=1600, strategy='go',toplot='only_avg') #6b
elif graph_list == 'traffic':
    # Group D: plots for diff data distribution 6040, 7030
    for dist in ['8020','7030','6040']:

        plot_thru_intra(data=1600,strategy='go',distribution=dist) # data in [1600,2400,3200], strategy in ['go','stay']
        plot_thru_inter(data=1600,strategy='go',distribution=dist)

        plot_thru_e2e(data=1600, strategy='go',distribution=dist)
        plot_delays_e2e(data=1600, strategy='go',toplot='only_avg',distribution=dist)
        plot_qdelays_e2e(data=1600, strategy='go',toplot='only_avg',distribution=dist)

        #plot_drop_comparison
    plot_delay_comparison(data=1600, strategy='go',toplot='only_avg',dist_list=['8020','7030','6040']) #7
elif graph_list=='strategy':
    # Group B: PLot for strategy (1600-go and stay variations)
    ###plot_delays_e2e(data=1600, strategy='go',toplot='all')
    ###plot_delays_e2e(data=1600, strategy='stay',toplot='all')
    plot_compare_delay_bar_B() #8

# Group C: PLot for scaling number of servers (1600,2400,3200 stay)
elif graph_list=='scaling':
    prepare_graphs=False
    if prepare_graphs:
        for data in [1600,2400,3200]:
            plot_delays_e2e(data=data, strategy='stay',toplot='only_hml') # toplot in ['only_avg', 'only_hml', 'all']
    else:
        data_list=[1600,2400,3200]
        plot_thru_per_server_intra_multiple(data_list=data_list,strategy='stay') # data in [1600,2400,3200], strategy in ['go','stay']         #9a
        plot_delay_multiple(data_list=data_list,strategy='stay') # data in [1600,2400,3200], strategy in ['go','stay']                     #9b

        plot_compare_delay_bar_C()                     #10

# test plot
#traffic_list=[8020,7030,6040]
#test_plot_stayin_intra_thru_drop(traffic_list=traffic_list)
#test_plot_stayin_intra_delays(traffic_list=traffic_list)

#test_plot_stayin_inter_thru_drop(traffic_list=traffic_list)
#test_plot_stayin_inter_delays(traffic_list=traffic_list)

#test_plot_stayin_brul_thru_drop(traffic_list=traffic_list)
#test_plot_stayin_brul_delays(traffic_list=traffic_list)

#test_plot_stayin_brdl_thru_drop(traffic_list=traffic_list)
#test_plot_stayin_brdl_delays(traffic_list=traffic_list)

#test_plot_stayin_e2e_thru_drop(traffic_list=traffic_list)
#test_plot_stayin_e2e_delays(traffic_list=traffic_list)

elif graph_list=='calabreta':
    ############ Calabreta Group A': Plots for basic scenario (1600-go with 800)
    prepare_graphs=False
    if prepare_graphs:
        #plot_thru_e2e(data=800, strategy='go')
        #plot_delays_e2e(data=800, strategy='go',toplot='only_avg')
        #plot_drop_prob(data=800, strategy='go')

        #plot_thru_e2e(data=1600, strategy='go')
        #plot_delays_e2e(data=1600, strategy='go',toplot='only_avg')
        #plot_drop_prob(data=1600, strategy='go')

        #plot_thru_e2e(data=800, strategy='stay')
        #plot_delays_e2e(data=800, strategy='stay',toplot='only_avg')
        #plot_drop_prob(data=800, strategy='stay')

        #plot_thru_e2e(data=1600, strategy='stay')
        #plot_delays_e2e(data=1600, strategy='stay',toplot='only_avg')
        #plot_drop_prob(data=1600, strategy='stay')

        plot_thru_e2e(data=400, strategy='go',setup='16x8')
        plot_delays_e2e(data=400, strategy='go',toplot='only_avg',setup='16x8')
        plot_drop_prob(data=400, strategy='go',setup='16x8')
    else:
        for rr in [2021,2022]:
            _comparison_date=rr
            plot_calabr_comparison(dt='thru')
            plot_calabr_comparison(dt='delay')
            plot_calabr_comparison(dt='loss')

