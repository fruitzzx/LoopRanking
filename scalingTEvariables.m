%scaling implementation

%load file
fromfile = load("localaveBROKEN3.txt");

[r, c] = size(fromfile)

for row = 1:1:r

	maxinrow = max(fromfile(row, :))*1.1;
	mininrow = min(fromfile(row, :))*0.9;		
	scales(row,1) = maxinrow - mininrow;
	
end

for i=1:1:c

	outfile(:,i) = fromfile(:,i)./scales;
	
end

save -ascii localaveBROKEN3scaled.txt outfile
	
			
			

