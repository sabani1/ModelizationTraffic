function a = blend_ACC(a_idm, a_cah, c)
if a_idm > a_cah
    a = a_idm;
else
    a = (1-c)*a_idm + c*a_cah;
end
