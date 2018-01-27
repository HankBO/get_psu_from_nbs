** ===========================================
**     导出stata 格式
** ===========================================
clear all

gl path /Users/BoHai/Desktop/get_psu_from_nbs/

insheet using $path/tmpfiles/province.txt, clear
drop if mi(v1)
ren v1 prov_name
gen prov_code = substr(v2,1,2)
drop v2
duplicates list prov_code
save $path/tmpfiles/prov.dta, replace

insheet using $path/tmpfiles/city.txt, clear
drop if mi(v1)
ren v1 city_name
gen city_code = substr(v2,4,4)
drop v2
duplicates list city_code
save $path/tmpfiles/city.dta, replace    //example: Hegang, 2304

** =======================================
**    County
** =======================================
** county 东莞，中山
clear
set obs 2
gen county_name = "东莞市" in 1
gen county_code = "441900" in 1
replace county_name = "中山市" in 2
replace county_code = "442000" in 2
save $path/tmpfiles/county_dongzhong.dta, replace

insheet using $path/tmpfiles/county.txt, clear
drop if mi(v1)
ren v1 county_name
gen county_code = substr(v2,4,6)
drop v2
append using $path/tmpfiles/county_dongzhong.dta
duplicates list county_code
save $path/tmpfiles/county.dta, replace

** =======================================
**    Town
** =======================================
insheet using $path/tmpfiles/dongzhong_town.txt, clear
save $path/tmpfiles/dongzhong_town.dta, replace

insheet using $path/tmpfiles/town.txt, clear
append using $path/tmpfiles/dongzhong_town.dta
drop if mi(v1)
ren v1 town_name
gen town_code = substr(v2,4,9)
drop v2
duplicates list town_code
save $path/tmpfiles/town.dta, replace

** =======================================
**    Village
** =======================================
insheet using $path/tmpfiles/dongzhong_village.txt, clear
save $path/tmpfiles/dongzhong_village.dta, replace

insheet using $path/tmpfiles/village.txt, clear
append using $path/tmpfiles/dongzhong_village.dta
format v1 %18.0g
tostring v1, replace usedisplayformat
ren v1 psu   //用village中的v1变量作为psu代码, 但是镇和村为空的不在village中
ren v2 community_name
ren v3 NBS_Type
gen prov_code = substr(psu,1,2)
gen city_code = substr(psu,1,4)
gen county_code = substr(psu,1,6)
gen town_code = substr(psu,1,9)
//把villiage_code为空的补上
merge m:1 town_code using $path/tmpfiles/town.dta
replace county_code=substr(town_code,1,6) if _merge==2 & length(town_code)==9
replace city_code=substr(town_code,1,4) if _merge==2 & length(town_code)==9
replace prov_code=substr(town_code,1,2) if _merge==2 & length(town_code)==9
replace psu=substr(town_code,1,.)+"000" if _merge==2 & length(town_code)==9
drop _merge
merge m:1 county_code using $path/tmpfiles/county.dta
//把town_code以及villiage_code为空的补上
replace town_code=substr(county_code,1,.)+"000" if _merge==2
replace city_code=substr(county_code,1,4) if _merge==2
replace prov_code=substr(county_code,1,2) if _merge==2
replace psu=substr(county_code,1,.)+"000000" if _merge==2
drop _merge
merge m:1 city_code using $path/tmpfiles/city.dta
drop _merge
merge m:1 prov_code using $path/tmpfiles/prov.dta
drop _merge
keep psu prov_name city_name county_name town_name community_name NBS_Type
order psu prov_name city_name county_name town_name community_name NBS_Type

label var psu "PSU"
label var prov_name "省"
label var city_name "市"
label var county_name "县"
label var town_name "乡镇"
label var community_name "村居"
compress
save $path/psu_2015.dta, replace

local tt prov city county town dongzhong_town dongzhong_village county_dongzhong
foreach x of local tt {
    erase $path/tmpfiles/`x'.dta
}

//gen post_need.dta
gen pstr = substr(prov_name,1,.)+substr(city_name,1,.)+substr(county_name,1,.)
duplicates drop
keep pstr
save $path/tmpfiles/post_need.dta, replace
