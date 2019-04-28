  SELECT ActiveOrder.Id as orderKey
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


  SELECT TOP 10000 [Id]
      ,[OrderId]
      ,[Description]
      ,[OrderLineId]
      ,[LineType]
      ,[JobId]
  FROM [LDSNG_Order_JP_Dev].[dbo].[Order_OrderLine]
  where [LineType] in (1, 2,3,4,7)