gyroData= csvread('fulltest.csv',7,0);

%%
start15 = find(gyroData(:,1) == 15);
end45 = find(gyroData(:,1) == 45);

start80 = find(gyroData(:,1) == 80);
end140 = find(gyroData(:,1) == 140);

start180 = find(gyroData(:,1) == 180);
end210 = find(gyroData(:,1) == 210);

start270 = find(gyroData(:,1) == 270);
end330 = find(gyroData(:,1) == 330);


dt = 1/128;

timevector = 0:dt:60;

%%

real33 = (33 + 1/3) * 360 * 1;
real45 = 45 * 360 * 1;
real0 = 0;

realcum33 = linspace(0, real33, 1+60*128);
realcum45 = linspace(0, real45, 1+60*128);
realcum0 = linspace(0, real0, 1+60*128);

%%

Xoffset = mean(gyroData(start15:end45,2));
Yoffset = mean(gyroData(start15:end45,3));
Zoffset = mean(gyroData(start15:end45,4));


XoffsetBis = mean(gyroData(start180:end210,2));
YoffsetBis = mean(gyroData(start180:end210,3));
ZoffsetBis = mean(gyroData(start180:end210,4));



%%
for i=2:4
    rot00(:,i-1) = cumtrapz(gyroData(start15:end45,1), ...
        (gyroData(start15:end45,i) - mean(gyroData(start15:end45,i))));
    rot33(:,i-1) = cumtrapz(gyroData(start80:end140,1), ...
        (gyroData(start80:end140,i) - mean(gyroData(start15:end45,i))));
    rot45(:,i-1) = cumtrapz(gyroData(start270:end330,1), ...
        (gyroData(start270:end330,i) - mean(gyroData(start180:end210,i))));
    rot00bis(:,i-1) = cumtrapz(gyroData(start180:end210,1), ...
        (gyroData(start180:end210,i) - mean(gyroData(start180:end210,i))));
end


%%
figure(1)
plot(timevector, realcum0,'LineWidth', 2)
hold on
plot(timevector(1:end/2+1), vecnorm(rot00'), '--','LineWidth', 1.5)
plot(timevector(1:end/2+1), vecnorm(rot00bis'), '--','LineWidth', 1.5)
plot(timevector, realcum33,'LineWidth', 2)
plot(timevector, vecnorm(rot33'), '--','LineWidth', 1.5)
plot(timevector, realcum45,'LineWidth', 2)
plot(timevector, vecnorm(rot45'), '--','LineWidth', 1.5)
hold off
legend('No movement', '0', '0bis', 'Real 33', '33', 'Real 45', '45', 'Location', 'NorthWest')

%%

diff0 = diff(realcum0(1:end/2+1)) - diff(vecnorm(rot00'));
diff0bis = diff(realcum0(1:end/2+1)) - diff(vecnorm(rot00bis'));
diff33 = diff(realcum33) - diff(vecnorm(rot33'));
diff45 = diff(realcum45) - diff(vecnorm(rot45'));

%%

figure(2)
subplot(2,1,1)
plot(timevector(2:end/2+1), diff0)
subplot(2,1,2)
[y,g] =lowpass(diff0,0.1);
plot(timevector(15:end/2-15), y(15:end-15))

figure(3)
subplot(2,1,1)
plot(timevector(2:end/2+1), diff0bis)
subplot(2,1,2)
[y,g] =lowpass(diff0bis,0.1);
plot(timevector(15:end/2-15), y(15:end-15))

figure(4)
subplot(2,1,1)
plot(timevector(2:end), diff33)
subplot(2,1,2)
[y,g] =lowpass(diff33,0.1);
plot(timevector(15:end-16), y(15:end-15))

figure(5)
subplot(2,1,1)
plot(timevector(2:end), diff45)
subplot(2,1,2)
[y,g] =lowpass(diff45,0.1);
plot(timevector(15:end-16), y(15:end-15))

m0 = mean(diff0);
m0bis = mean(diff0bis);
m33 = mean(diff33);
m45 = mean(diff45);

%%

[pxx, w] = periodogram(diff33-mean(diff33),[],[],128);
figure(6)
plot(w, pxx);

[pxx, w] = periodogram(diff45-mean(diff45),[],[],128);
figure(7)
plot(w, pxx);

[pxx, w] = periodogram(diff0-mean(diff0),[],[],128);
figure(8)
plot(w, pxx);


%%
x = [0,33+1/3,45];
mean0 = mean([m0, m0bis]);
y = [mean0, m33, m45];
[p,S] = polyfit(x,y,1);
x1 = linspace(0,45,1000);
y1 = polyval(p, x1);
figure(10)
plot(x,y,'x')
hold on
plot(x1,y1, '-')
hold off

R = corrcoef(x,y)

