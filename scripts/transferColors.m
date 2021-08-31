sourcePath = '..\resources\MaSTr1325\'; % path to source images - for example MaSTr1325
sourceImages = dir([sourcePath, '*.jpg*']);
targetPath = '..\images\'; % path to generated sythetic images
targetImages = dir([targetPath, '*mage*']);
Ns = length(sourceImages);
Nt = length(targetImages);

sourceImages.name
targetImages.name

for i = 1:Nt
    targetImages(i).name
    sourceImage = imread([sourcePath, sourceImages(randi(Ns)).name]);
    targetImage = imread([targetPath, targetImages(i).name]);
    out = CT(double(sourceImage)/255, double(targetImage)/255);
    imwrite(out, [targetPath, targetImages(i).name])
end
    