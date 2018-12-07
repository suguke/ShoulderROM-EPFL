load('MiniProjectData.mat')
%%
Mouse_Names = {'TK473', 'TK490', 'TK532', 'TK539', 'TK545', 'TK364', 'TK407', 'TK478', 'TK479', 'TK479', 'TK355', 'TK358', 'TK471', 'TK472', 'TK506', 'TK454', 'TK455', 'TK461', 'TK462', 'TK523'};
Cells = [1 1 1 1 2 1 1 1 1 2 1 2 1 1 2 1 2 1 2 2];
Trials = [4 4 3 2 3 4 4 3 4 5 3 6 4 2 2 2 4 3 2 3];

Frequency = [];
AP_threshold = [];
AP_Amplitude = [];
AP_mean_dur = [];
Mean_Vm = [];
STD_Vm = [];

FFT_EXC = [];
FFT_PV = [];
FFT_SST = [];
FFT_VIP = [];


for k = 1:length(Mouse_Names)
    Mouse_Name = Mouse_Names{k};
    Cell = Cells(k);
    Trial = Trials(k);

    Whichone = (strcmp(data.Mouse_Name, Mouse_Name) & (data.Cell_Counter == Cell) & (data.Trial_Counter == Trial));

    Membrane_Potential = data.Trial_MembranePotential{Whichone};
    Time_Vector = (1:length(Membrane_Potential))/40000;

    [AP_Picks, AP_Time] = findpeaks(Membrane_Potential,Time_Vector,  'MinPeakHeight', -20, 'MinPeakProminence', 10);

    Frequency(k) = size(AP_Time, 2)/Time_Vector(end);

    Diff = diff(Membrane_Potential);

    Diff = Diff*10^(-3)*40000;

    Flag = Diff >= 10;

    Time_step = 1;

    [Der_amp, Der_time] = findpeaks(double(Flag), 'MinPeakDistance', Time_step*10^(-3)*40000);

    AP_threshold_index = [];
    for i = 1:length(AP_Time)
        Diff = abs(AP_Time(i)*40000-Der_time);
        [~, Min_Pos] = min(Diff);
        AP_threshold_index(i) = Der_time(Min_Pos);
    end

    AP_thr_All = Membrane_Potential(AP_threshold_index);
    AP_threshold(k) = mean(AP_thr_All);

    AP_Amplitude_all = AP_Picks - AP_thr_All;
    AP_Amplitude(k) = mean(AP_Amplitude_all);

    AP_half_mean = AP_threshold(k) + (AP_Amplitude(k)/2);

    AP_duration = [];
    VM_More_AP_half = Membrane_Potential >= AP_half_mean;
    Last = VM_More_AP_half(1);
    Time = 0;
    for i = 2:length(VM_More_AP_half)
        if (Last == 0) &  (VM_More_AP_half(i) == 1)
            Time = 1;
        elseif (Last == 1) & (VM_More_AP_half(i) == 1)
            Time = Time + 1;
        elseif (Last == 1) & (VM_More_AP_half(i) == 0)
            AP_duration = [AP_duration Time];
            Time = 0;
        end
        Last = VM_More_AP_half(i);
    end

    AP_duration = AP_duration/40000;
    AP_mean_dur(k) = mean(AP_duration);

    Vm = Membrane_Potential(Membrane_Potential < AP_threshold(k));

    Mean_Vm(k) = mean(Vm);
    STD_Vm(k) = std(Vm);
    
    FFT_ = [];
    start = 1;
    end_ = 80000;
    for i = 1:15
        Vm_2sec = Membrane_Potential(start:end_);
        FFT_(i, :) = abs(fft(Vm_2sec));
        start = end_ + 1;
        end_ = end_ + 80000;
    end
    
    if (k >= 1) & (k <= 5)
        FFT_EXC(size(FFT_EXC, 1)+1, :) = mean(FFT_, 1);
    elseif (k > 5) & (k <= 10)
        FFT_PV(size(FFT_PV, 1)+1, :) = mean(FFT_, 1);
    elseif (k > 10) & (k <= 15)
        FFT_SST(size(FFT_SST, 1)+1, :) = mean(FFT_, 1);
    elseif (k > 15) & (k <= 20)
        FFT_VIP(size(FFT_VIP, 1)+1, :) = mean(FFT_, 1);
    end
    
    freq = 0:40000/80000:80000/2;

    figure(k)
    plot(freq(1:(end-1)), mean(FFT_, 1))
    hold on
    xlabel('Frequency (Hz)')
    ylabel('Amplitude')
    set(gca, 'xlim', [0.5 15])
    
    disp(k)
end
%%
figure()
plot(freq(1:(end-1)), mean(FFT_EXC, 1), 'k', 'LineWidth', 2)
hold on
plot(freq(1:(end-1)), mean(FFT_PV, 1), 'r', 'LineWidth', 2)
plot(freq(1:(end-1)), mean(FFT_SST, 1), 'y', 'LineWidth', 2)
plot(freq(1:(end-1)), mean(FFT_VIP, 1), 'b', 'LineWidth', 2)
xlabel('Frequency (Hz)')
ylabel('Amplitude')
legend('EXC', 'PV', 'SST', 'VIP')
set(gca, 'xlim', [0.5 20])
    
    


