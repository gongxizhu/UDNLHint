select OrderLinesArchive.OrderId,
  --JobDesc=STUFF((
		--	SELECT ',' + JobArchive.[Description]
		--	FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive
		--	WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Id = OrderLinesArchive.Id
		--	FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		--1, 1, ''), 
  --OrderArchive.Notes as OrderNotes, 
  STUFF((
			SELECT ',' + A.[Description]
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as A
			WHERE max(OrderLinesArchive.OrderId) = A.OrderId
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '') as LineDesc
  --,
  --LaborItemArchive.DATId, 
  --LaborItemArchive.LaborId,
  --OrderLinesArchive.LineType
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive as LaborItemArchive
  on LaborItemArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] as OrderArchive
  on OrderArchive.Id = OrderLinesArchive.OrderId
  where OrderLinesArchive.OrderId in (
	  select top 1000 ArchiveOrder.Id  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] as ArchiveOrder left join
	  [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] as VehicleDetailsArchive
	  on ArchiveOrder.Id = VehicleDetailsArchive.Id
	  where ChassisNumber like 'CD%' 
	  or ChassisNumber like 'CG%' 
	  or ChassisNumber like 'JNCU%' 
	  and MakeCode = 'UD' 
	  and OrderType = 1 
	  and OrderId <11657012
	  order by OrderId
  )
  and OrderLinesArchive.LineType in (2, 3, 4, 7)
  group by OrderLinesArchive.OrderId
  order by OrderLinesArchive.OrderId
  --order by JobArchive.[Description], JobArchive.OrderId, JobArchive.Id
  
-- Find Job descs
SELECT Id as OrderId
	   ,JobDesc=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Description
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
FROM
(
	SELECT DISTINCT TOP 1000 OrderArchive.Id as Id
		--,OrderArchive.Notes
		--,JobArchive.Description AS JobDesc
		--,OrderArchive.Notes AS OrderNotes
		--,OrderLinesArchive.Description AS LineDesc
		--,JobArchive.Id AS JobId
		--,OrderLinesArchive.Id AS LineId
		--,LaborItemArchive.DATId
		--,LaborItemArchive.LaborId
		--,OrderLinesArchive.LineType
	FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive
	LEFT JOIN 
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive
	ON OrderArchive.Id = OrderLinesArchive.OrderId
	LEFT JOIN
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive
	ON OrderArchive.Id = VehicleDetailsArchive.Id
	WHERE ChassisNumber like 'CD%' 
		OR ChassisNumber like 'CG%' 
		OR ChassisNumber like 'JNCU%' 
		AND MakeCode = 'UD' 
		AND OrderType = 1 
		AND OrderArchive.Id < 11657012
		AND OrderLinesArchive.LineType in (2, 3, 4, 7)
	ORDER BY OrderArchive.Id
) AS SelectedOrders
GROUP BY SelectedOrders.Id
ORDER BY SelectedOrders.Id

-- Find Line descs
SELECT Id as OrderId
	   ,LineDesc=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].Description
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive]
			WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].OrderId = SelectedOrders.Id
			AND [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].LineType in (2, 3, 4, 7)
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
FROM
(
	SELECT DISTINCT TOP 1000 OrderArchive.Id as Id
		--,OrderArchive.Notes
		--,JobArchive.Description AS JobDesc
		--,OrderArchive.Notes AS OrderNotes
		--,OrderLinesArchive.Description AS LineDesc
		--,JobArchive.Id AS JobId
		--,OrderLinesArchive.Id AS LineId
		--,LaborItemArchive.DATId
		--,LaborItemArchive.LaborId
		--,OrderLinesArchive.LineType
	FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive
	LEFT JOIN 
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive
	ON OrderArchive.Id = OrderLinesArchive.OrderId
	LEFT JOIN
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive
	ON OrderArchive.Id = VehicleDetailsArchive.Id
	WHERE ChassisNumber like 'CD%' 
		OR ChassisNumber like 'CG%' 
		OR ChassisNumber like 'JNCU%' 
		AND MakeCode = 'UD' 
		AND OrderType = 1 
		AND OrderArchive.Id < 11657012
		AND OrderLinesArchive.LineType in (2, 3, 4, 7)
	ORDER BY OrderArchive.Id
) AS SelectedOrders
GROUP BY SelectedOrders.Id
ORDER BY SelectedOrders.Id


-- Find Order Notes
SELECT DISTINCT TOP 1000 OrderArchive.Id as Id
		,Notes
		--,OrderArchive.Notes
		--,JobArchive.Description AS JobDesc
		--,OrderArchive.Notes AS OrderNotes
		--,OrderLinesArchive.Description AS LineDesc
		--,JobArchive.Id AS JobId
		--,OrderLinesArchive.Id AS LineId
		--,LaborItemArchive.DATId
		--,LaborItemArchive.LaborId
		--,OrderLinesArchive.LineType
FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive
LEFT JOIN 
[LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive
ON OrderArchive.Id = OrderLinesArchive.OrderId
LEFT JOIN
[LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive
ON OrderArchive.Id = VehicleDetailsArchive.Id
WHERE ChassisNumber like 'CD%' 
		OR ChassisNumber like 'CG%' 
		OR ChassisNumber like 'JNCU%' 
		AND MakeCode = 'UD' 
		AND OrderType = 1 
		AND OrderArchive.Id < 11657012
		AND OrderLinesArchive.LineType in (2, 3, 4, 7)
	ORDER BY OrderArchive.Id



-- Find Line Details
SELECT Id as OrderId
	   ,Notes=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Notes
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Id = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
	   ,JobDesc=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Description
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
	   ,LineDesc=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].Description
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive]
			WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].OrderId = SelectedOrders.Id
			AND [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].LineType in (2, 3, 4, 7)
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
	   ,Parts=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.PartNumber
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,DATs=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.DATId
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,STDs=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.LaborId
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
FROM
(
	SELECT DISTINCT TOP 1000 OrderArchive.Id as Id
		--,OrderArchive.Notes
		--,JobArchive.Description AS JobDesc
		--,OrderArchive.Notes AS OrderNotes
		--,OrderLinesArchive.Description AS LineDesc
		--,JobArchive.Id AS JobId
		--,OrderLinesArchive.Id AS LineId
		--,LaborItemArchive.DATId
		--,LaborItemArchive.LaborId
		--,OrderLinesArchive.LineType
	FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive
	LEFT JOIN 
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive
	ON OrderArchive.Id = OrderLinesArchive.OrderId
	LEFT JOIN
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive
	ON OrderArchive.Id = VehicleDetailsArchive.Id
	WHERE ChassisNumber like 'CD%' 
		OR ChassisNumber like 'CG%' 
		OR ChassisNumber like 'JNCU%' 
		AND MakeCode = 'UD' 
		AND OrderType = 1 
		AND OrderArchive.Id < 11657012
		AND OrderLinesArchive.LineType in (2, 3, 4, 7)
	ORDER BY OrderArchive.Id
) AS SelectedOrders
GROUP BY SelectedOrders.Id
ORDER BY SelectedOrders.Id


SELECT Id as OrderId
	   ,Notes=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Notes
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive.Id = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		+ ',' + STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Description
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		+ ',' + STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].Description
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive]
			WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].OrderId = SelectedOrders.Id
			AND [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].LineType in (2, 3, 4, 7)
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
	 --  ,JobDesc=STUFF((
		--	SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.Description
		--	FROM [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive
		--	WHERE [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive.OrderId = SelectedOrders.Id
		--	FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		--1, 1, '')
	 --  ,LineDesc=STUFF((
		--	SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].Description
		--	FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive]
		--	WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].OrderId = SelectedOrders.Id
		--	AND [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive].LineType in (2, 3, 4, 7)
		--	FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		--1, 1, '')
	   ,Parts=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.PartNumber
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,DATs=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.DATId
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,STDs=STUFF((
			SELECT ',' + [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.LaborId
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive
			LEFT JOIN [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			ON [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.Id = [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive.Id
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,Straights=(SELECT COUNT(*)
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			AND LineType = 4
		)
		,TextAmmounts=(SELECT COUNT(*)
			FROM [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive
			WHERE [LDSNG_Order_JP_Dev].[dbo].Order_OrderLineArchive.OrderId = SelectedOrders.Id
			AND LineType = 7
		)
FROM
(
	SELECT DISTINCT TOP 10 OrderArchive.Id as Id
		--,OrderArchive.Notes
		--,JobArchive.Description AS JobDesc
		--,OrderArchive.Notes AS OrderNotes
		--,OrderLinesArchive.Description AS LineDesc
		--,JobArchive.Id AS JobId
		--,OrderLinesArchive.Id AS LineId
		--,LaborItemArchive.DATId
		--,LaborItemArchive.LaborId
		--,OrderLinesArchive.LineType
	FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] AS OrderArchive
	LEFT JOIN 
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] AS OrderLinesArchive
	ON OrderArchive.Id = OrderLinesArchive.OrderId
	LEFT JOIN
	[LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetailsArchive] AS VehicleDetailsArchive
	ON OrderArchive.Id = VehicleDetailsArchive.Id
	WHERE ChassisNumber like 'CD%' 
		OR ChassisNumber like 'CG%' 
		OR ChassisNumber like 'JNCU%' 
		AND MakeCode = 'UD' 
		AND OrderType = 1 
		AND OrderArchive.Id < 11657012
		AND OrderLinesArchive.LineType in (2, 3, 4, 7)
	ORDER BY OrderArchive.Id
) AS SelectedOrders
GROUP BY SelectedOrders.Id
ORDER BY SelectedOrders.Id