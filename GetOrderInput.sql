-- Part
SELECT OrderArchive.Notes as OrderDesc
	  ,OrderLinesArchive.[Description] as LineDesc
      ,JobArchive.[Description] as JobDesc
	  ,LineType
	  ,PartNumber
	  ,OrderLinesArchive.OrderId
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_PartLineArchive as PartLinesArchive
  on PartLinesArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive as OrderArchive
  on OrderLinesArchive.OrderId = OrderArchive.Id 
  where [LineType] = 1 -- (1, 2, 3, 4, 7)
  and OrderLinesArchive.OrderId in (
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
  and OrderLinesArchive.[Description] is not null 
  and OrderLinesArchive.[Description] <> ''
  order by OrderLinesArchive.OrderId



-- DAT
SELECT OrderArchive.Notes as OrderDesc
	  ,OrderLinesArchive.[Description] as LineDesc
      ,JobArchive.[Description] as JobDesc
	  ,OrderLinesArchive.LineType
	  ,DATId
	  ,LaborId
	  ,OrderLinesArchive.OrderId
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive as LaborItemArchive
  on LaborItemArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive as OrderArchive
  on OrderLinesArchive.OrderId = OrderArchive.Id 
  where OrderLinesArchive.[LineType] = 2 -- (1, 2, 3, 4, 7)
  and OrderLinesArchive.OrderId in (
	  select top 2000 ArchiveOrder.Id  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] as ArchiveOrder left join
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
  --and OrderLinesArchive.[Description] is not null 
  --and OrderLinesArchive.[Description] <> ''
  order by OrderLinesArchive.OrderId


  -- SDT
SELECT OrderArchive.Notes as OrderDesc
	  ,OrderLinesArchive.[Description] as LineDesc
      ,JobArchive.[Description] as JobDesc
	  ,OrderLinesArchive.LineType
	  ,DATId
	  ,LaborId
	  ,OrderLinesArchive.OrderId
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive as LaborItemArchive
  on LaborItemArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive as OrderArchive
  on OrderLinesArchive.OrderId = OrderArchive.Id 
  where OrderLinesArchive.[LineType] = 3 -- (1, 2, 3, 4, 7)
  and OrderLinesArchive.OrderId in (
	  select top 2000 ArchiveOrder.Id  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderArchive] as ArchiveOrder left join
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
  and OrderLinesArchive.[Description] is not null 
  and OrderLinesArchive.[Description] <> ''
  order by OrderLinesArchive.OrderId


    -- Straight
SELECT OrderArchive.Notes as OrderDesc
	  ,OrderLinesArchive.[Description] as LineDesc
      ,JobArchive.[Description] as JobDesc
	  ,OrderLinesArchive.LineType
	  ,DATId
	  ,LaborId
	  ,OrderLinesArchive.OrderId
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_LaborItemArchive as LaborItemArchive
  on LaborItemArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive as OrderArchive
  on OrderLinesArchive.OrderId = OrderArchive.Id 
  where OrderLinesArchive.[LineType] = 4 -- (1, 2, 3, 4, 7)
  and OrderLinesArchive.OrderId in (
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
  and OrderLinesArchive.[Description] is not null 
  and OrderLinesArchive.[Description] <> ''
  order by OrderLinesArchive.OrderId


   -- Text Amount
SELECT OrderArchive.Notes as OrderDesc
	  ,OrderLinesArchive.[Description] as LineDesc
      ,JobArchive.[Description] as JobDesc
	  ,LineType
	  ,FixedAmount
	  ,Cost
	  ,OrderLinesArchive.OrderId
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
  left join [LDSNG_Order_JP_Dev].[dbo].Order_TextAmountLineArchive as TextAmountLineArchive
  on TextAmountLineArchive.Id = OrderLinesArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_JobArchive as JobArchive
  on OrderLinesArchive.OrderId = JobArchive.OrderId 
  and OrderLinesArchive.JobId = JobArchive.Id
  left join [LDSNG_Order_JP_Dev].[dbo].Order_OrderArchive as OrderArchive
  on OrderLinesArchive.OrderId = OrderArchive.Id 
  where OrderLinesArchive.[LineType] = 7 -- (1, 2, 3, 4, 7)
  and OrderLinesArchive.OrderId in (
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
  and OrderLinesArchive.[Description] is not null 
  and OrderLinesArchive.[Description] <> ''
  order by OrderLinesArchive.OrderId



  select JobArchive.*, OrderArchive.Notes, OrderLinesArchive.LineType, OrderLinesArchive.[Description], LaborItemArchive.DATId, LaborItemArchive.LaborId  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLineArchive] as OrderLinesArchive
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
  order by JobArchive.[Description], JobArchive.OrderId, JobArchive.Id