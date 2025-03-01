% Load the data
filename = '2024-10-25.csv';

data = readtable(filename, 'VariableNamingRule', 'preserve'); % Preserve original column names

% outliers = isoutlier(data(:, 2));  
% 
% clean_data = data(~outliers, :);
% 
% csvwrite('cleaned_data.csv', clean_data);

% Convert time to datetime format
data.("Time measured") = datetime(data.("Time measured"), 'InputFormat', 'yyyy/MM/dd HH:mm:ss');

% Plot temperature, relative humidity, ambient light, and sound noise against time
figure;

% Subplot 1: Temperature
subplot(2,2,1);
plot(data.("Time measured"), data.Temperature, 'r', 'LineWidth', 2);
title('Temperature Over Time');
xlabel('Time');
ylabel('Temperature (°C)');
grid on;

% Subplot 2: Ambient Light
subplot(2,2,2);
plot(data.("Time measured"), data.("Ambient light"), 'b', 'LineWidth', 2);
title('Ambient Light Over Time');
xlabel('Time');
ylabel('Ambient Light (lux)');
grid on;

% Subplot 3: Sound Noise
subplot(2,2,3);
plot(data.("Time measured"), data.("Sound noise"), 'k', 'LineWidth', 2);
title('Sound Noise Over Time');
xlabel('Time');
ylabel('Sound Noise (dB)');
grid on;

% Adjust layout for clarity
sgtitle('Environmental Parameters Over Time');