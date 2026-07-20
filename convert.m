load('Pupil_dataset.mat')
S = Pupil_data;
for i = 1:numel(S)
    S(i).epocs = table2struct(S(i).Task_epocs, 'ToScalar', true);
end
S = rmfield(S, {'Task_epocs','Task_data'});
save('Pupil_clean.mat', 'S', '-v7');
