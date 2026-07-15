-- ТОП-10 репозиториев по форкам
select name, forks
from repositories
order by forks desc
limit 10;

-- ТОП-10 репозиториев по звездам
select name, stars
from repositories
order by forks desc
limit 10;

-- распределение репозиториев по языкам
select l.name, count(*)
from repositories r
join languages l on (r.language_id = l.id)
group by l.name;

-- среднее количество stars по языкам
select l.name, round(avg(r.stars), 2) as avg_stars 
from repositories r
join languages l on (r.language_id = l.id)
group by l.name;

-- количество репозиториев каждого владельца
select o.name as owner, count(*) as repo_count
from repositories r
join owners o on (r.owner_id = o.id)
group by o.name

-- количество commits по репозиториям
select r.name as repo_name, count(c.sha) as commits_count
from repositories r
left join commits c on (c.repository_id = r.id)
group by r.name

-- количество issues по репозиториям
select r.name as repo_name, count(i.id) as issues_count
from repositories r
left join issues i on (i.repository_id = r.id)
group by r.name

-- процент открытых/закрытых issues
select r.name as repo_name,
round(count(*) filter (where state='open') * 100.0 / count(*), 2) as open_issues_share,
round(count(*) filter (where state='closed') * 100.0 / count(*), 2) as closed_issues_share
from repositories r
join issues i on (i.repository_id = r.id)
group by r.name

-- репозитории без коммитов
select r.name as repo_name, count(c.sha) as commits_count
from repositories r
left join commits c on (c.repository_id = r.id)
group by r.name
having count(c.sha) = 0

-- среднее время жизни issue в репозитории
select r.name as repo_name, 
avg(extract(epoch from (i.closed_at - i.created_at)))::int / 86400  as avg_close_issue_days
from issues i
join repositories r on (r.id = i.repository_id) 
where state = 'closed'
group by r.name

-- среднее число коммитов на репозиторий
select trunc(avg(repo_commits)) as avg_commits_count
from (
	select count(c.sha) as repo_commits
	from repositories r
	left join commits c on (c.repository_id = r.id)
	group by r.name
)