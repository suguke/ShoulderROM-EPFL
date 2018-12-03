gyroData= csvread('gyroLongTest.csv',7,0);


start80 = find(gyroData(:,1) == 80);
end140 = find(gyroData(:,1) == 140);
start140 = end140;
end200 = find(gyroData(:,1) == 200);
start200 = end200;
end260 = find(gyroData(:,1) == 260);



dt = 1/128;

for i=2:4
    rot80140(:,i-1) = cumtrapz(gyroData(start80:end140,1), gyroData(start80:end140,i));
    rot140200(:,i-1) = cumtrapz(gyroData(start140:end200,1), gyroData(start140:end200,i));
    rot200260(:,i-1) = cumtrapz(gyroData(start200:end260,1), gyroData(start200:end260,i));
end

realRotation = (33 + 1/3) * 360 * 1;

%%
realcumrot = linspace(0, realRotation, 1+60*128);





figure(1)
plot(vecnorm(rot80140'))
hold on
plot(vecnorm(rot140200'))
plot(vecnorm(rot200260'))
plot(realcumrot)
hold off
legend('1','2','3', 'real')

%%

Xoffset = median(gyroData(1:3315,2))
Yoffset = median(gyroData(1:3315,3))
Zoffset = median(gyroData(1:3315,4))


gyroNoOffset = gyroData(:,1:4) - repmat([0 Xoffset Yoffset Zoffset], ...
    [size(gyroData,1),1]);

for i=2:4
    rotNO80140(:,i-1) = cumtrapz(gyroNoOffset(start80:end140,1), gyroNoOffset(start80:end140,i));
    rotNO140200(:,i-1) = cumtrapz(gyroNoOffset(start140:end200,1), gyroNoOffset(start140:end200,i));
    rotNO200260(:,i-1) = cumtrapz(gyroNoOffset(start200:end260,1), gyroNoOffset(start200:end260,i));
end

figure(1)
hold on
plot(vecnorm(rotNO80140'), '--')
plot(vecnorm(rotNO140200'), '--')
plot(vecnorm(rotNO200260'), '--')
hold off
legend('1','2','3', 'real', 'n1','n2', 'n3', 'Location', 'northwest')
title('Cumulative angles')

%% 

figure(2)
plot(realcumrot - vecnorm(rot80140'))
hold on
plot(realcumrot - vecnorm(rotNO80140'))
hold off
legend('with offset', 'without offset')
title('Difference between theoretical and measured angles')

figure(2)
subplot(2,1,1)
plot((diff(realcumrot) - diff(vecnorm(rot140200'))))
title('Variation of the offset during time')
subplot(2,1,2)
[y,g] =lowpass((diff(realcumrot) - diff(vecnorm(rot140200'))),0.1);
plot(20:7680-20, y(20:end-20))
title('with lowpass')
% monSignal = diff(realcumrot) - diff(vecnorm(rot140200'));
monSignal = gyroData(start140:end200,4);

[pxx, w] = periodogram(monSignal-mean(monSignal),[],[],128);
figure(3)
plot(w, pxx);