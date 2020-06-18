The dataset is composed of two .mat files:

- "/trajectories_data/traces.mat" contains the "traces_data" matrix, an Nx10 matrix which columns refer to:
	-- 1: time of the measurement in seconds;
	-- 2: vehicle ID;
	-- 3: absolute x coordinate of the vehicle location in meters;
	-- 4: absolute y coordinate of the vehicle location in meters;
	-- 5: speed of the vehicle in meters over second;
	-- 6: hexagonal cell associated with the x-y location (i.e., serving base station (BS));
	-- 7: hexagonal cell to which the user will be connected in the next time step;
	-- 8: hexagonal cell visited before the current one (cell C - 1) no matter how much time before (i.e., previous serving BS);
	-- 9: hexagonal cell C - 2;
	-- 10: hexagonal cell C - 3;
	N is the number of collected traces.
	A negative number in columns 7, 8, 9 or 10 is referred to time steps out of the recorded trajectory.

- "/trajectories_data/coordinate_BS.mat" contains the "BSCoordinates" matrix, an Mx2 matrix which columns refer to:
	-- 1: absolute x coordinate of the BS location in meters;
	-- 2: absolute y coordinate of the BS location in meters;
	M is the number of hexagonal cells in which the city is divided.

prova prova
prova2 prova2