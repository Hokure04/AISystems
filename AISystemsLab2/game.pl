% ключевые персонажи игры
character(knight).
character(false_knight).
character(hornet).
character(mantis_lords).
character(soul_master).
character(nosk).
character(collector).
character(betrayed_lord).
character(lost_brother).
character(trem_mother).
character(dung_guard).
character(hollow_knight).
character(iselda).
character(sly).
character(foot_eater).
character(mighty_zot).
character(quirell).
character(cloth).
character(tiso).
character(effulgence).

% персонажи являющиеся странниками
wanderer(cloth).
wanderer(quirell).
wanderer(tiso).
wanderer(knight).
wanderer(mighty_zot).

% персонажи имеющие высокий показатель здоровья
high_health(false_knight).
high_health(hornet).
high_health(mantis_lords).
high_health(soul_master).
high_health(nosk).
high_health(collector).
high_health(betrayed_lord).
high_health(lost_brother).
high_health(trem_mother).
high_health(effulgence).

% факты о том, какой персонаж одолел другого
defeated_by(false_knight, knight).
defeated_by(hornet, knight).
defeated_by(mantis_lords, knight).
defeated_by(soul_master, knight).
defeated_by(nosk, knight).
defeated_by(collector, knight).
defeated_by(betrayed_lord, knight).
defeated_by(lost_brother, knight).
defeated_by(trem_mother, knight).
defeated_by(betrayed_lord, cloth).
defeated_by(cloth, betrayed_lord).
defeated_by(effulgence, knight).

% доступные способности
abilities(moth_cape).
abilities(mantis_claw).
abilities(crystal_heart).
abilities(monarch_wings).
abilities(izma_tear).
abilities(shadow_cape).
abilities(king_brade).
abilities(dreams_gate).
abilities(dream_sword).

% факты о том, какими способностями обладает персонаж
have(knight, moth_cape).
have(knight, mantis_claw).
have(knight, crystal_heart).
have(knight, monarch_wings).
have(knight, izma_tear).
have(knight, shadow_cape).
have(knight, king_brade).
have(knight, dreams_gate).
have(knight, dream_sword).

have(effulgence, eight_rays).
have(effulgence, twelve_nails).
have(effulgence, nails_collapse).
have(effulgence, nails_wave).
have(effulgence, heavenly_ray).
have(effulgence, golden_spheres).

% факты о том, какие персонажи помогали друг другу на протяжении игры
helped_in_journey(hornet, knight).
helped_in_journey(iselda, knight).
helped_in_journey(sly, knight).
helped_in_journey(foot_eater, knight).
helped_in_journey(cloth, knight).
helped_in_journey(quirell, knight).
helped_in_journey(knight, cloth).
helped_in_journey(knight, sly).
helped_in_journey(knight, mighty_zot).
helped_in_journey(dung_guard, knight).
helped_in_journey(quirell, knight).

% правило для подсчёта количества способностей
count_abilities(X, Count):-
    findall(A, have(X,A), Abilities),
    length(Abilities, Count).

% правило для определения того, является ли персонаж главным героем
is_main_character(X):-
    character(knight),
    wanderer(X),
    count_abilities(X, Count),
    Count =:= 9.

% правило для определения того, является ли персонаж боссом
is_boss(X):-
    defeated_by(X,Y),
    high_health(X),
    character(X),
    is_main_character(Y).

% правило для определения одолели ли пермонажи друг друга
defeat_each_other(X,Y):-
    defeated_by(X,Y),
    defeated_by(Y,X).

% правило для определения союзников персонажа
is_ally(X,Y):-
    character(X),
    character(Y),
    (helped_in_journey(X,Y) ; helped_in_journey(Y,X)),
    !.

% правило для определения тог является ли персонаж главным боссом
is_final_boss(X):-
    character(X),
    is_boss(X),
    count_abilities(X, Count),
    Count =:= 6.
