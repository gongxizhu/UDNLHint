  SELECT top 1 ActiveOrder.Id as orderKey
		,ActiveOrder.OrderId
		,Notes
		,VehicleType
		,[RegistrationNumber]
		,ServiceTypeCode
      ,[ChassisNumber]
      ,[ModelNumber]
      ,[MakeCode]
      ,[MakeCodeDescription]
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_Order] as ActiveOrder left join
  [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetails] as VehicleDetails
  on ActiveOrder.Id = VehicleDetails.Id
  where ChassisNumber like 'CD%' 
  or ChassisNumber like 'CG%' 
  or ChassisNumber like 'JNCU%' 
  and MakeCode = 'UD'


  SELECT [Id]
      ,[OrderId]
      ,[Description]
      ,[OrderLineId]
      ,[LineType]
      ,[JobId]
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine]
  where [LineType] in (1, 2,3,4,7)
  and OrderId in (
  select ActiveOrder.Id  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_Order] as ActiveOrder left join
  [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetails] as VehicleDetails
  on ActiveOrder.Id = VehicleDetails.Id
  where ChassisNumber like 'CD%' 
  or ChassisNumber like 'CG%' 
  or ChassisNumber like 'JNCU%' 
  and MakeCode = 'UD')
  order by OrderId



    SELECT top 10 ActiveOrder.Id as orderKey
		,ActiveOrder.OrderId
		,Notes
		,LineDesc=STUFF((
			SELECT ',' + OrderLine.[Description]
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine]
			WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine].OrderId = ActiveOrder.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
		,LineType=STUFF((
			SELECT ',' + CONVERT(nvarchar, OrderLine.LineType)
			FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine]
			WHERE [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine].OrderId = ActiveOrder.Id
			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 
		1, 1, '')
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_Order] as ActiveOrder left join
  [LDSNG_Order_JP_Dev].[dbo].[Order_OrderVehicleDetails] as VehicleDetails
  on ActiveOrder.Id = VehicleDetails.Id
  right join [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine] as OrderLine
  on ActiveOrder.Id = OrderLine.OrderId
  where (ChassisNumber like 'CD%' 
  or ChassisNumber like 'CG%' 
  or ChassisNumber like 'JNCU%') 
  and MakeCode = 'UD'
  and OrderLine.LineType in (1,2,3,4,7)
  --group by ActiveOrder.OrderId
  order by ActiveOrder.OrderId