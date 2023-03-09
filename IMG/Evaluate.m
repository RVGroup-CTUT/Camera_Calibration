%function Distance = Evaluate(num_image,name_image,p1,p2) 
%Choose image for calculating
num_image = 19 %from Camera calibrator app
name_image = 'img36.png' %from the directory store your image (checker board)

%Get IntrinsicMatrix and transpose
T=cameraParams.IntrinsicMatrix';
%Get distance from camera to work plane
Z=cameraParams.TranslationVectors(num_image,3);
%Get posititons of projectedPoint in your image (checker board)
[imagePoints] = detectCheckerboardPoints(name_image);
%Choose 2 numbers of imagePoints which you want to calculate distance
FirstPoint = 6;
SecondPoint = 3;

P1=[imagePoints(FirstPoint,:),1]';%Image position - pixel
m1=inv(T)*Z*P1;%Real position - mm 
P2=[imagePoints(SecondPoint,:),1]';%Image position - pixel
m2=inv(T)*Z*P2;%Real position - mm 
%Calculate distance from 
Distance=sqrt((m1(1,1)-m2(1,1))^2+(m1(2,1)-m2(2,1))^2+(m1(3,1)-m2(3,1))^2)
%end