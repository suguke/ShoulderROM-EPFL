gyroData= csvread('gyroLongTest.csv',7,0);


start80 = find(gyroData(:,1) == 80);
end140 = find(gyroData(:,1) == 140);
start140 = end140;
end200 = find(gyroData(:,1) == 200);
start200 = end200;
end260 = find(gyroData(:,1) == 260);



dt = 1/128;

timevector = 0:1/128:60;

for i=2:4
    rot80140(:,i-1) = cumtrapz(gyroData(start80:end140,1), gyroData(start80:end140,i));
    rot140200(:,i-1) = cumtrapz(gyroData(start140:end200,1), gyroData(start140:end200,i));
    rot200260(:,i-1) = cumtrapz(gyroData(start200:end260,1), gyroData(start200:end260,i));
end

realRotation = (33 + 1/3) * 360 * 1;

%%
realcumrot = linspace(0, realRotation, 1+60*128);





figure(1)
plot(timevector, realcumrot)
hold on
plot(timevector, vecnorm(rot80140'))
plot(timevector, vecnorm(rot140200'))
plot(timevector, vecnorm(rot200260'))
hold off

%%

Xoffset = mean(gyroData(1:3315,2))
Yoffset = mean(gyroData(1:3315,3))
Zoffset = mean(gyroData(1:3315,4))


gyroNoOffset = gyroData(:,1:4) - repmat([0 Xoffset Yoffset Zoffset], ...
    [size(gyroData,1),1]);

for i=2:4
    rotNO80140(:,i-1) = cumtrapz(gyroNoOffset(start80:end140,1), gyroNoOffset(start80:end140,i));
    rotNO140200(:,i-1) = cumtrapz(gyroNoOffset(start140:end200,1), gyroNoOffset(start140:end200,i));
    rotNO200260(:,i-1) = cumtrapz(gyroNoOffset(start200:end260,1), gyroNoOffset(start200:end260,i));
end

figure(1)
hold on
plot(timevector, vecnorm(rotNO80140'), '--')
plot(timevector, vecnorm(rotNO140200'), '--')
plot(timevector, vecnorm(rotNO200260'), '--')
hold off
axis tight
legend('Theoretical', '80-140','140-200','200-260', '80-140, offset correction', ...
    '140-200, offset correction','200-260, offset correction','Location', 'northwest')
title('Theoretical and experimental cumulative angles from gyroscope')

%% 

figure(2)
plot(realcumrot - vecnorm(rot80140'))
hold on
plot(realcumrot - vecnorm(rotNO80140'))
hold off
legend('with offset', 'without offset')
title('Difference between theoretical and measured angles')
%%
monSignal = diff(realcumrot) - diff(vecnorm(rot140200'));

figure(2)
subplot(2,1,1)
plot(timevector(2:end), monSignal)
title('Variation of the offset during time')
axis tight
subplot(2,1,2)
[y,g] =lowpass(monSignal,0.1);
plot(timevector(15:end-16), y(15:end-15))
title('with lowpass')
axis tight
%%
monSignal = gyroData(start140:end200,4);

[pxx, w] = periodogram(monSignal-mean(monSignal),[],[],128);
figure(3)
plot(w, pxx);


freq = 0:1/128:60;

figure(4)
plot(freq, abs(fft(monSignal-mean(monSignal))))

%%
figure(5)
plot(timevector(2:end), diff(vecnorm(rot140200')))
hold on
plot(timevector(2:end), diff(realcumrot))